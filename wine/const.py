from collections import namedtuple

COUNTRY_DATA = [
    ('ZA', "South Africa", ),
    ('AU', "Australia"),
    ('NZ', "New Zealand"),
    ('FR', "France"),
    ('ES', "Spain"),
    ('IT', "Italy"),
    ('US', "United States"),
    ('AR', "Argentina"),
    ('CL', "Chile"),
]


class Country(namedtuple('Country', ['code', 'name'])):

    def to_model_choice(self):
        # for use in model "choices"
        return self.code, self.name


def _make_country(country_tuple):
    return Country(country_tuple[0], country_tuple[1])

COUNTRIES = [_make_country(c) for c in COUNTRY_DATA]

def get_all_country_choices():
    return [c.to_model_choice() for c in COUNTRIES]
