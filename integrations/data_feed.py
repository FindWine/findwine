from collections import namedtuple

WINE_DATA_ATTRIBUTES = (
    "id",
    "name",
    "url",
    "price",
    "stock_amount",
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
