from collections import namedtuple
import xml.etree.ElementTree as ET


XML_NAMES_TO_ATTRIBUTES = {
    "Category": "category",
    "Id": "id",
    "Manufacturer": "manufacturer",
    "Wine": "wine",
    "Vintage": "vintage",
    "ProductName": "productname",
    "Volume": "volume",
    "ProductURL": "producturl",
    "StockAvailability": "stockavailability",
    "Price": "price",
    "DeliveryCost": "deliverycost",
    "Currency": "currency",
}

class WineData(namedtuple('WineData', sorted(XML_NAMES_TO_ATTRIBUTES.values()))):
    pass


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
