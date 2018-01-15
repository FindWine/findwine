from collections import namedtuple
import xml.etree.ElementTree as ET
from django.core.mail import mail_admins
import requests
from integrations.exceptions import FeedUpdateError
from wine.models import MerchantWine, Merchant


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
    skipped = []
    not_found = []
    for wine_data in get_port2port_data(get_raw_feed()):
        wine, work_done = apply_update(wine_data)
        if wine is not None:
            if work_done:
                results[wine] = work_done
            else:
                skipped.append(wine)
        else:
            not_found.append(wine_data)
    subject, pretty_results = _get_printed_results(results, skipped, not_found)
    if debug:
        print(subject)
        print(pretty_results)
    else:
        mail_admins(subject, pretty_results)


def get_raw_feed():
    FEED_URL = 'https://www.port2port.wine/findwine.xml'
    r = requests.get(FEED_URL)
    r.encoding = 'utf-8'
    return requests.get(FEED_URL).text


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
                raise FeedUpdateError("Prevented change of external ID for {} from {} to {}.".format(
                    wine, wine.external_id, wine_data.id
                ))
            wine.external_id = wine_data.id
            work_done.append('Added external ID {}'.format(wine_data.id))

        if wine_data.product_url and wine.url != wine_data.product_url:
            work_done.append('Changed URL from {} to {}'.format(wine.url, wine_data.product_url))
            wine.url = wine_data.product_url

        is_available = bool(wine_data.stock_availability and wine_data.stock_availability != '0')
        if wine.available != is_available:
            wine.available = is_available
            work_done.append('Set available to {} based on a stock of {}'.format(is_available,
                                                                                 wine_data.stock_availability))
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
        skipped='\nNo updates applied to {} wines'.format(len(skipped)),
        missing='\n{} wines were not found in FindWine database:\n{}'.format(
            len(not_found),
            '\n'.join(['\t{}'.format(w) for w in not_found])
        )
    )
    return subject, body


def _update_to_result(wine, work_done):
    return '\t{}\n{}'.format(wine, '\n'.join(['\t\t{}'.format(w) for w in work_done]))
