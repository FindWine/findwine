import xml.etree.ElementTree as ET
from decimal import Decimal
import requests

from integrations.data_feed import WineData, apply_update
from integrations.util import notify_data_team
from wine.models import MerchantWine, Merchant


FEED_URL = 'https://www.port2port.wine/findwine.xml'
PORT2PORT_MERCHANT_NAME = 'Port2Port'
XML_NAMES_TO_ATTRIBUTES = {
    "Id": "id",
    "ProductName": "name",
    "ProductURL": "url",
    "StockAvailability": "stock_amount",
    "Price": "price",
}


def update_all(debug=False):
    """
    Updates all data based on the results of the port2port feed.
    """
    results = {}
    found = set()
    skipped = []
    not_found = []
    # first pass - update everything in the feed
    for wine_data in get_port2port_data(get_raw_feed()):
        wine, work_done = apply_update(wine_data, debug)
        if wine is not None:
            found.add(wine.pk)
            if work_done:
                results[wine] = work_done
            else:
                skipped.append(wine)
        else:
            not_found.append(wine_data)

    # second pass - update all available wines that no longer show up in the feed
    for existing_wine in MerchantWine.objects.filter(merchant=get_port2port_merchant(), available=True):
        if existing_wine.pk not in found:
            existing_wine.available = False
            results[existing_wine] = ['Set available to False because it was missing from the feed.']
            if not debug:
                existing_wine.save()

    subject, pretty_results = _get_printed_results(results, skipped, not_found)
    if debug:
        print(subject)
        print(pretty_results)
    else:
        notify_data_team(subject, pretty_results)


def get_raw_feed():
    r = requests.get(FEED_URL)
    r.encoding = 'utf-8'
    return requests.get(FEED_URL).content


def get_port2port_data(raw_feed):
    root = ET.fromstring(raw_feed)
    for child in root:
        yield _element_to_data(child)


def _element_to_data(feed_item):
    vals = {
        elem_id: feed_item.find(elem_name).text
        for elem_name, elem_id in XML_NAMES_TO_ATTRIBUTES.items()
    }
    vals['merchant_name'] = PORT2PORT_MERCHANT_NAME
    return WineData(**vals)


def get_port2port_merchant():
    return Merchant.objects.get(name=PORT2PORT_MERCHANT_NAME)


def _get_printed_results(results, skipped, not_found):
    total_number_processed = len(results) + len(skipped) + len(not_found)
    subject = 'Successfully processed {}/{} results from Port2Port Feed'.format(len(results),
                                                                                total_number_processed)
    body = '{updated}\n{skipped}\n{missing}'.format(
        updated='\nApplied the following {} updates: \n{}'.format(
            len(results),
            '\n'.join([_update_to_result(wine, work_done) for wine, work_done in results.items()])
        ),
        skipped='\nNo updates applied to {} wines:\n{}'.format(
            len(skipped),
            '\n'.join(['\t{}'.format(w) for w in skipped])
        ),
        missing='\n{} wines were not found in FindWine database:\n{}'.format(
            len(not_found),
            '\n'.join(['\t{}'.format(w) for w in not_found])
        )
    )
    return subject, body


def _update_to_result(wine, work_done):
    return '\t{}\n{}'.format(wine, '\n'.join(['\t\t{}'.format(w) for w in work_done]))
