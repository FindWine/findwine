import json
from collections import Counter

from decimal import Decimal

from integrations.data_feed import process_wine_feed, get_raw_feed, WineData
from wine.models import Merchant

FEED_URL = 'https://www.vinoteque.co.za/products.json'
LIMIT = 250
VINOTEQUE_MERCHANT_NAME = 'Vinoteque'


def update_all(debug=False):
    """
    Updates all data based on the results of the port2port feed.
    """
    page = 1
    while True:
        query_string = 'limit={}&page={}'.format(LIMIT, page)
        url = '{}?{}'.format(FEED_URL, query_string)
        feed_json = get_raw_feed(url, as_json=True)
        all_wine_datas = list(get_vinoteque_data(feed_json))
        if not all_wine_datas:
            break
        merchant = Merchant.objects.get(name=VINOTEQUE_MERCHANT_NAME)
        process_wine_feed(merchant, all_wine_datas, debug=debug)
        page += 1


def get_vinoteque_data(feed):
    for product in feed['products']:
        yield vinoteque_product_to_data(product)


def vinoteque_product_to_data(product):
    variant_to_use = _get_variant_to_use(product['variants'])
    return WineData(
        id=product['id'],
        name=product['title'],
        url=_get_url(product),
        price=_get_price(variant_to_use),
        # this is just used to set availability on our side anyways
        stock_amount=1 if variant_to_use['available'] else 0,
        merchant_name=VINOTEQUE_MERCHANT_NAME,
    )


def _get_variant_to_use(variants):
    for variant in variants:
        quantity, size = _get_quantity_and_size_from_variant_title(variant['title'])
        variant['quantity'] = quantity
        variant['size'] = size

    def _get_variant_sort_key(variant):
        # available comes before unavailable
        available_param = 0 if variant['available'] else 1
        quantity_param = 0 if variant['quantity'] == 1 else 1 if variant['quantity'] == 6 else 2
        size_param = 0 if variant['size'] == '750ml' else 1
        return (available_param, quantity_param, size_param)

    return sorted(variants, key=_get_variant_sort_key)[0]


def _get_quantity_and_size_from_variant_title(title):
    """
    This takes data from the variant's title (e.g. '1x750ml' or '6x750ml || Mature') and
    turns it into explicit params on the variant itself.
    """
    quantity, remainder = title.lower().split('x')
    quantity = int(quantity)
    size = remainder.split(' ')[0]
    return quantity, size


def _get_url(product):
    return 'https://www.vinoteque.co.za/products/{}'.format(product['handle'])


def _get_price(variant):
    # todo: need to account for if it is a case of 6
    return str(round(Decimal(variant['price']) / variant['quantity'], 2))
