from django.test import TestCase
from wine.models import Producer, Wine, WineVintage
from wine.tests.test_util import bootstrap_categories
from wine.util import generate_slug_from_parts, generate_slug


class WineVintageSlugTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(WineVintageSlugTest, cls).setUpClass()
        cls.producer = Producer(name='Warwick')
        cls.producer.save()
        cls.wine = Wine(producer=cls.producer, name='Grey Lady')
        cls.wine.save()
        cls.category, cls.subcategory = bootstrap_categories()

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

    def test_slug_generated_on_save(self):
        vintage = WineVintage(wine=self.wine, year=2015, category=self.category, sub_category=self.subcategory)
        vintage.save()
        self.assertEqual('warwick-grey-lady-2015', vintage.slug)
        self.assertEqual(vintage.pk, WineVintage.objects.get(slug='warwick-grey-lady-2015').pk)

    def test_slug_uniqueness(self):
        vintage = WineVintage(wine=self.wine, year=2015, category=self.category, sub_category=self.subcategory)
        vintage.save()
        self.assertEqual('warwick-grey-lady-2015', vintage.slug)
        vintage2 = WineVintage(wine=self.wine, year=2015, category=self.category, sub_category=self.subcategory)
        vintage2.save()
        self.assertEqual('warwick-grey-lady-2015-2', vintage2.slug)
        vintage3 = WineVintage(wine=self.wine, year=2015, category=self.category, sub_category=self.subcategory)
        vintage3.save()
        self.assertEqual('warwick-grey-lady-2015-3', vintage3.slug)
