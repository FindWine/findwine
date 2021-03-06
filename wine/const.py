from collections import namedtuple


SOUTH_AFRICA_CODE = 'ZA'
SOUTH_AFRICAN_RAND_CODE = 'ZAR'


# To add a country you can copy the format below.
# For the metadata fields you can add:
# 'is_producer': False to add a country that should not show up in wine choices
# 'is_merchant': True to add a country that should show up in merchant choices
# 'currency': 'XXX' to set a merchant country's currency
COUNTRY_DATA = [
    (SOUTH_AFRICA_CODE, "South Africa", {'is_merchant': True, 'currency': SOUTH_AFRICAN_RAND_CODE}),
    ('AR', "Argentina"),
    ('AU', "Australia", {'is_merchant': True, 'currency': 'AUD'}),
    ('CL', "Chile"),
    ('CN', "China"),
    ('FR', "France"),
    ('IT', "Italy"),
    ('LB', "Lebanon"),
    ('NZ', "New Zealand"),
    ('PT', "Portugal"),
    ('ES', "Spain"),
    ('GB', "United Kingdom", {'is_merchant': True, 'currency': 'GBP'}),
    ('US', "United States", {'is_merchant': True, 'currency': 'USD'}),
]



class Country(namedtuple('Country', ['code', 'name', 'is_producer', 'is_merchant', 'currency'])):

    def to_model_choice(self):
        # for use in model "choices"
        return self.code, self.name

    def to_currency_choice(self):
        return self.currency, self.name


def _make_country(country_tuple):
    metadata = {}
    if len(country_tuple) > 2:
        assert len(country_tuple) == 3
        metadata = country_tuple[2]

    return Country(country_tuple[0], country_tuple[1], metadata.get('is_producer', True),
                   metadata.get('is_merchant', False), metadata.get('currency', None))

COUNTRIES = [_make_country(c) for c in COUNTRY_DATA]


def get_all_country_choices():
    return [c.to_model_choice() for c in COUNTRIES]


def get_all_country_wine_choices():
    return [c.to_model_choice() for c in COUNTRIES if c.is_producer]


def get_all_merchant_country_choices():
    return [c.to_model_choice() for c in COUNTRIES if c.is_merchant]


def get_all_currency_choices():
    return [c.to_currency_choice() for c in COUNTRIES if c.is_merchant]
