from collections import namedtuple
import xml.etree.ElementTree as ET
import requests
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
    "StockAvailability": "stockavailability",
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


def get_raw_feed():
    FEED_URL = 'https://www.port2port.wine/findwine.xml'
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


def apply_update(wine_data):
    wine = get_wine_for_data(wine_data)
    if wine:
        pass


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
