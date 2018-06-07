import xml.etree.ElementTree as ET
import requests
from decimal import Decimal

from integrations.data_feed import WineData, process_wine_feed, shared_element_to_data
from wine.models import Merchant


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
    return process_wine_feed(get_port2port_merchant(), all_wine_datas,
                             # custom_processor=update_minimum_purchase_unit,
                             debug=debug)


def get_raw_feed():
    r = requests.get(FEED_URL)
    r.encoding = 'utf-8'
    return requests.get(FEED_URL).content


def get_port2port_data(raw_feed):
    root = ET.fromstring(raw_feed)
    for child in root:
        yield _element_to_data(child)


def _element_to_data(feed_item):
    return shared_element_to_data(feed_item, XML_NAMES_TO_ATTRIBUTES, PORT2PORT_MERCHANT_NAME)


def get_port2port_merchant():
    return Merchant.objects.get(name=PORT2PORT_MERCHANT_NAME)


def update_minimum_purchase_unit(wine_data, wine, work_done):
    price = Decimal(wine_data.price) if wine_data.price else None
    if price:
        purchase_unit = 6 if price < 150 else 1
        # temporarily disable purchase unit logic
        if wine.minimum_purchase_unit != purchase_unit and purchase_unit == 6:
            work_done.append('Set minimum purchase unit from {} to {}'.format(wine.minimum_purchase_unit, purchase_unit))
            wine.minimum_purchase_unit = purchase_unit
