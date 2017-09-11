from django.test import TestCase
from wine.models import Producer, Wine, WineVintage
from wine.util import generate_slug_from_parts, generate_slug


class WineVintageSlugTest(TestCase):

    def test_formatting(self):
        TEST_CASES = (
            (('Bouchard Finlayson', 'Galpin Peak', 2015), 'bouchard-finlayson-galpin-peak-2015'),
            (("Apostrophe's", "And other spec!@l C#arachters", 2015), 'apostrophes-and-other-specl-carachters-2015'),
            (("   leading and ", " trailing whitespace    ", 2015), 'leading-and-trailing-whitespace-2015'),
            ((None, None, 2015), 'unknown-producer-unknown-wine-2015'),
            (('', '', 2015), 'unknown-producer-unknown-wine-2015'),
        )
        for inputs, expected_output in TEST_CASES:
            self.assertEqual(expected_output, generate_slug_from_parts(*inputs))

    def test_slugs_from_fields(self):
        producer = Producer(name='Warwick')
        wine = Wine(producer=producer, name='Grey Lady')
        vintage = WineVintage(wine=wine, year=2015)
        self.assertEqual(generate_slug(vintage), 'warwick-grey-lady-2015')
