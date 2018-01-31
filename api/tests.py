from decimal import Decimal
from django.test import SimpleTestCase
from api.util import coerce_to_decimal


class CoerceToDecimalTest(SimpleTestCase):

    def test_basics(self):
        for val in (0, '0', '1.2', '3.58'):
            self.assertEqual(Decimal(val), coerce_to_decimal(val))

    def test_unhandleable(self):
        for val in (None, 'abc', '1.2.3', ['0'], {}):
            self.assertEqual(None, coerce_to_decimal(val))

    def test_lenient(self):
        for input, output in [
            ('1a', 1),
            ('w100', 100),
            ('x1.2x13x', '1.213'),
        ]:
            self.assertEqual(Decimal(output), coerce_to_decimal(input))
