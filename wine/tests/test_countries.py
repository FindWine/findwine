from django.test import SimpleTestCase

# Create your tests here.
from wine.const import get_all_merchant_country_choices, get_all_country_wine_choices, get_all_currency_choices


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
