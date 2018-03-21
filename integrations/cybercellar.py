import xml.etree.ElementTree as ET

import requests

from integrations.data_feed import process_wine_feed
from integrations.port2port import WineData
from wine.models import Merchant

FEED_URL = 'https://www.cybercellar.com/media/find_wine.xml'
CYBERCELLAR_MERCHANT_NAME = 'Cybercellar'
XML_NAMES_TO_ATTRIBUTES = {
    "id": "id",
    "name": "name",
    "url": "url",
    "price": "price",
    "stock_level": "stock_amount",
}


def update_all(debug=False):
    """
    Updates all data based on the results of the port2port feed.
    """
    all_wine_datas = get_cybercellar_data(get_raw_feed())
    merchant = Merchant.objects.get(name=CYBERCELLAR_MERCHANT_NAME)
    return process_wine_feed(merchant, all_wine_datas, debug=debug)


def get_cybercellar_data(raw_feed):
    root = ET.fromstring(raw_feed)
    for child in root:
        yield _element_to_data(child)


def _element_to_data(feed_item):
    vals = {
        elem_id: feed_item.find(elem_name).text.strip()
        for elem_name, elem_id in XML_NAMES_TO_ATTRIBUTES.items()
    }
    vals['merchant_name'] = CYBERCELLAR_MERCHANT_NAME
    return WineData(**vals)


def get_raw_feed():
    r = requests.get(FEED_URL)
    r.encoding = 'utf-8'
    return requests.get(FEED_URL).content

