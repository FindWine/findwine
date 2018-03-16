from collections import namedtuple
import xml.etree.ElementTree as ET
from decimal import Decimal
import requests
from integrations.util import notify_data_team
from wine.models import MerchantWine, Merchant


FEED_URL = 'https://www.port2port.wine/findwine.xml'
PORT2PORT_MERCHANT_NAME = 'Port2Port'
XML_NAMES_TO_ATTRIBUTES = {
    "Category": "category",
    "Id": "id",
    "Manufacturer": "manufacturer",
    "Wine": "wine",
    "Vintage": "vintage",
    "ProductName": "productname",
    "Volume": "volume",
    "ProductURL": "product_url",
    "StockAvailability": "stock_availability",
    "Price": "price",
    "DeliveryCost": "deliverycost",
    "Currency": "currency",
}


class WineData(namedtuple('WineData', sorted(XML_NAMES_TO_ATTRIBUTES.values()))):
    # https://stackoverflow.com/a/16721002/8207
    __slots__ = ()

    def __new__(cls, **kwargs):
        new_kwargs = {
            v: None for v in XML_NAMES_TO_ATTRIBUTES.values()
        }
        new_kwargs.update(kwargs)
        return super(WineData, cls).__new__(cls, **new_kwargs)

    def __str__(self):
        return '{} ({}, {})'.format(self.wine, self.id, self.product_url)


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
    return WineData(**vals)


def apply_update(wine_data, debug=False):
    wine = get_wine_for_data(wine_data)
    work_done = []
    if wine:
        if wine.external_id != wine_data.id:
            if wine.external_id:
                work_done.append('Changed external ID from {} to {}'.format(wine.external_id, wine_data.id))
            else:
                work_done.append('Added external ID {}'.format(wine_data.id))
            wine.external_id = wine_data.id
        if wine_data.product_url and wine.url != wine_data.product_url:
            work_done.append('Changed URL from {} to {}'.format(wine.url, wine_data.product_url))
            wine.url = wine_data.product_url

        is_available = bool(wine_data.stock_availability and wine_data.stock_availability != '0')
        if wine.available != is_available:
            wine.available = is_available
            work_done.append('Set available to {} based on a stock of {}'.format(is_available,
                                                                                 wine_data.stock_availability))
        price = Decimal(wine_data.price) if wine_data.price else None
        if price and wine.price != price:
            work_done.append('Changed price from {} to {}'.format(wine.price, price))
            wine.price = price
        if price:
            purchase_unit = 6 if price < 150 else 1
            # temporarily disable purchase unit logic
            if wine.minimum_purchase_unit != purchase_unit and purchase_unit == 6 and False:
                work_done.append('Set minimum purchase unit from {} to {}'.format(wine.minimum_purchase_unit, purchase_unit))
                wine.minimum_purchase_unit = purchase_unit

        if work_done and not debug:
            wine.save()
    return wine, work_done


def get_port2port_merchant():
    return Merchant.objects.get(name=PORT2PORT_MERCHANT_NAME)


def get_wine_for_data(wine_data):
    merchant = get_port2port_merchant()
    try:
        return MerchantWine.objects.get(merchant=merchant, external_id=wine_data.id)
    except MerchantWine.DoesNotExist:
        try:
            return MerchantWine.objects.get(merchant=merchant, url=wine_data.product_url)
        except MerchantWine.DoesNotExist:
            return None


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
