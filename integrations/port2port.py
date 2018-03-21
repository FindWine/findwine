import xml.etree.ElementTree as ET
import requests

from integrations.data_feed import WineData, apply_update, process_wine_feed
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
    all_wine_datas = get_port2port_data(get_raw_feed())
    return process_wine_feed(get_port2port_merchant(), all_wine_datas, debug=debug)


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
