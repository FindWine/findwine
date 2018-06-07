import xml.etree.ElementTree as ET

from integrations.data_feed import shared_element_to_data
from integrations import port2port

FEED_URL = 'http://winecellar.co.za/find-wine-xml/'
WINECELLAR_MERCHANT_NAME = 'Wine Cellar'


def get_winecellar_data(raw_feed):
    root = ET.fromstring(raw_feed)
    for child in root:
        yield shared_element_to_data(child, port2port.XML_NAMES_TO_ATTRIBUTES, WINECELLAR_MERCHANT_NAME)
