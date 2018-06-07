import xml.etree.ElementTree as ET

from integrations.data_feed import shared_element_to_data, process_wine_feed, get_raw_feed
from integrations import port2port
from wine.models import Merchant

FEED_URL = 'http://winecellar.co.za/find-wine-xml/'
WINECELLAR_MERCHANT_NAME = 'Wine Cellar'


def update_all(debug=False):
    """
    Updates all data based on the results of the port2port feed.
    """
    all_wine_datas = get_winecellar_data(get_raw_feed(FEED_URL))
    merchant = Merchant.objects.get(name=WINECELLAR_MERCHANT_NAME)
    return process_wine_feed(merchant, all_wine_datas, debug=debug)


def get_winecellar_data(raw_feed):
    root = ET.fromstring(raw_feed)
    for child in root:
        yield shared_element_to_data(child, port2port.XML_NAMES_TO_ATTRIBUTES, WINECELLAR_MERCHANT_NAME)
