import json

from integrations.data_feed import process_wine_feed, get_raw_feed, WineData
from wine.models import Merchant

FEED_URL = 'https://www.vinoteque.co.za/products.json?limit=250&page=1'
VINOTEQUE_MERCHANT_NAME = 'Vinoteque'


def update_all(debug=False):
    """
    Updates all data based on the results of the port2port feed.
    """
    all_wine_datas = get_vinoteque_data(get_raw_feed(FEED_URL))
    merchant = Merchant.objects.get(name=VINOTEQUE_MERCHANT_NAME)
    return process_wine_feed(merchant, all_wine_datas, debug=debug)


def get_vinoteque_data(raw_feed):
    feed = json.loads(raw_feed)
    for product in feed['products']:
        yield vinoteque_product_to_data(product)


def vinoteque_product_to_data(product):
    variant_to_use = _get_variant_to_use(product)
    return WineData(
        id=product['id'],
        name=product['title'],
        url=_get_url(product),
        price=_get_price(variant_to_use),
        # this is just used to set availability on our side anyways
        stock_amount=1 if variant_to_use['available'] else 0,
        merchant_name=VINOTEQUE_MERCHANT_NAME,
    )


def _get_variant_to_use(product):
    # todo: may need to be smarter to accommodate for different quantities
    # currently assumes we should use the first available one
    for variant in product['variants']:
        if variant['available']:
            return variant
    return product['variants'][0]


def _get_url(product):
    return 'https://www.vinoteque.co.za/products/{}'.format(product['handle'])


def _get_price(variant):
    # todo: need to account for if it is a case of 6
    return variant['price']
