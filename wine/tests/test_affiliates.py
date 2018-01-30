from django.test import TestCase
from wine.models import Merchant, MerchantWine
from wine.tests.test_util import get_a_new_wine_vintage


class WineVintageSlugTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(WineVintageSlugTest, cls).setUpClass()
        cls.wine = get_a_new_wine_vintage()
        cls.merchant = Merchant.objects.create(name='Test Merchant', priority=1)
        cls.wine_url = 'http://www.example.com/a-nice-wine/'
        cls.merchant_wine = MerchantWine(merchant=cls.merchant, wine_vintage=cls.wine, url=cls.wine_url)

    def setUp(self):
        self.merchant.affiliate_params = {}
        self.merchant.save()

    @classmethod
    def tearDownClass(cls):
        super(WineVintageSlugTest, cls).tearDownClass()
        cls.wine.delete()
        cls.merchant.delete()

    def test_default(self):
        self.assertEqual(self.wine_url, self.merchant_wine.get_url())

    def test_with_params(self):
        self.merchant.affiliate_params = {
            'p1': 'foo',
            'p2': 'bar',
        }
        self.assertEqual('http://www.example.com/a-nice-wine/?p2=bar&p1=foo', self.merchant_wine.get_url())
