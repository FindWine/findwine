from django.test import SimpleTestCase

# Create your tests here.
from geoposition import Geoposition
from wine.const import get_all_merchant_country_choices, get_all_country_wine_choices, get_all_currency_choices
from wine.geoposition import geoposition_to_dms_string


EXPECTED_WINE_CHOICES = [
    ('ZA', "South Africa"),
    ('AU', "Australia"),
    ('NZ', "New Zealand"),
    ('FR', "France"),
    ('ES', "Spain"),
    ('IT', "Italy"),
    ('GB', "United Kingdom"),
    ('US', "United States"),
    ('AR', "Argentina"),
    ('CL', "Chile"),
]

EXPECTED_MERCHANT_CHOICES = [
    ('ZA', "South Africa"),
    ('AU', "Australia"),
    ('GB', "United Kingdom"),
    ('US', "United States"),
]

EXPECTED_CURRENCY_CHOICES = [
    ('ZAR', "South Africa"),
    ('AUD', "Australia"),
    ('GBP', "United Kingdom"),
    ('USD', "United States"),
]


class CountriesTest(SimpleTestCase):

    def test_all_choices(self):
        self.assertEqual(EXPECTED_WINE_CHOICES, get_all_country_wine_choices())

    def test_all_merchants(self):
        self.assertEqual(EXPECTED_MERCHANT_CHOICES, get_all_merchant_country_choices())

    def test_all_currencies(self):
        self.assertEqual(EXPECTED_CURRENCY_CHOICES, get_all_currency_choices())


class GeopositionTest(SimpleTestCase):

    def test_simple(self):
        self.assertEqual('''S 33° 49' 20.92" E 18° 55' 48.51"''',
                         geoposition_to_dms_string(Geoposition(-33.8224777, 18.9301428)))
