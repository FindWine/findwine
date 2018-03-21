from collections import namedtuple

from decimal import Decimal

from wine.models import Merchant, MerchantWine

WINE_DATA_ATTRIBUTES = (
    "id",
    "name",
    "url",
    "price",
    "stock_amount",
    "merchant_name",
)


class WineData(namedtuple('WineData', WINE_DATA_ATTRIBUTES)):
    # https://stackoverflow.com/a/16721002/8207
    __slots__ = ()

    def __new__(cls, **kwargs):
        new_kwargs = {
            v: None for v in WINE_DATA_ATTRIBUTES
        }
        new_kwargs.update(kwargs)
        return super(WineData, cls).__new__(cls, **new_kwargs)

    def __str__(self):
        return '{} ({}, {})'.format(self.name, self.id, self.url)

    @property
    def merchant(self):
        try:
            return Merchant.objects.get(name=self.merchant_name)
        except Merchant.DoesNotExist:
            return None


def apply_update(wine_data, debug=False):
    wine = get_wine_for_data(wine_data)
    work_done = []
    if wine:
        if wine.external_id != wine_data.id:
            if wine.external_id:
                work_done.append('Changed external ID from {} to {}'.format(wine.external_id, wine_data.id))
            else:
                work_done.append('Added external ID {}'.format(wine_data.id))
            wine.external_id = wine_data.id
        if wine_data.url and wine.url != wine_data.url:
            work_done.append('Changed URL from {} to {}'.format(wine.url, wine_data.url))
            wine.url = wine_data.url

        is_available = bool(wine_data.stock_amount and wine_data.stock_amount != '0')
        if wine.available != is_available:
            wine.available = is_available
            work_done.append('Set available to {} based on a stock of {}'.format(is_available,
                                                                                 wine_data.stock_amount))
        price = Decimal(wine_data.price) if wine_data.price else None
        if price and wine.price != price:
            work_done.append('Changed price from {} to {}'.format(wine.price, price))
            wine.price = price
        if price:
            purchase_unit = 6 if price < 150 else 1
            # temporarily disable purchase unit logic
            if wine.minimum_purchase_unit != purchase_unit and purchase_unit == 6 and False:
                work_done.append('Set minimum purchase unit from {} to {}'.format(wine.minimum_purchase_unit, purchase_unit))
                wine.minimum_purchase_unit = purchase_unit

        if work_done and not debug:
            wine.save()
    return wine, work_done


def get_wine_for_data(wine_data):
    assert wine_data.merchant is not None
    try:
        return MerchantWine.objects.get(merchant=wine_data.merchant, external_id=wine_data.id)
    except MerchantWine.DoesNotExist:
        try:
            return MerchantWine.objects.get(merchant=wine_data.merchant, url=wine_data.url)
        except MerchantWine.DoesNotExist:
            return None
