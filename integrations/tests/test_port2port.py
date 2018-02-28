import os
from unittest import skip
from decimal import Decimal
from django.test import SimpleTestCase, TestCase
from integrations.exceptions import FeedUpdateError
from integrations.port2port import get_port2port_data, PORT2PORT_MERCHANT_NAME, get_wine_for_data, WineData, \
    apply_update, update_all
from wine.models import MerchantWine, Merchant
from wine.tests.test_util import get_a_new_wine_vintage


class Port2PortFeedTest(SimpleTestCase):

    def test_parse_feed(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'port2port-feed.xml')) as f:
            raw_feed = f.read()

        data = list(get_port2port_data(raw_feed))
        self.assertEqual(2, len(data))
        wine_info = data[0]
        self.assertEqual('Wine', wine_info.category)
        self.assertEqual('2261', wine_info.id)
        self.assertEqual('Arendsig', wine_info.manufacturer)
        self.assertEqual('1000 Vines Viognier', wine_info.wine)
        self.assertEqual('2016', wine_info.vintage)
        self.assertEqual('Arendsig 1000 Vines Viognier 2016', wine_info.productname)
        self.assertEqual('750 ml', wine_info.volume)
        self.assertEqual('https://www.port2port.wine/buy-wine/arendsig/1000-vines-viognier-2016',
                         wine_info.product_url)
        self.assertEqual('56', wine_info.stock_availability)
        self.assertEqual('150.00', wine_info.price)
        self.assertEqual('120', wine_info.deliverycost)
        self.assertEqual('ZAR', wine_info.currency)


class Port2PortFeedDbTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(Port2PortFeedDbTest, cls).setUpClass()
        cls.merchant = Merchant.objects.create(name=PORT2PORT_MERCHANT_NAME, priority=1)
        cls.wine_vintage = get_a_new_wine_vintage()
        cls.merchant_wine = MerchantWine.objects.create(
            merchant=cls.merchant, wine_vintage=cls.wine_vintage, minimum_purchase_unit=1,
            external_id='test_id', url='http://test.com/wine-url',
        )

    def test_get_no_match(self):
        self.assertEqual(None, get_wine_for_data(WineData()))
        self.assertEqual(None, get_wine_for_data(WineData(product_url='missing', id='missing')))

    def test_get_by_id(self):
        self.assertEqual(self.merchant_wine, get_wine_for_data(WineData(id=self.merchant_wine.external_id)))

    def test_get_by_url(self):
        self.assertEqual(self.merchant_wine, get_wine_for_data(WineData(product_url=self.merchant_wine.url)))

    def test_get_wrong_merchant(self):
        bogus_merchant_wine = MerchantWine.objects.create(
            merchant=Merchant.objects.create(name='bogus', priority=1),
            wine_vintage=self.wine_vintage, minimum_purchase_unit=1,
            external_id='bogus_id', url='http://test.com/bogus-wine-url'
        )
        self.addCleanup(bogus_merchant_wine.delete)
        self.assertEqual(None, get_wine_for_data(WineData(id=bogus_merchant_wine.external_id,
                                                          product_url=bogus_merchant_wine.url)))

    def test_set_external_id_if_null(self):
        url = 'test_set_external_id_if_null_url'
        id = 'test_set_external_id_if_null_id'
        wine = MerchantWine.objects.create(
            merchant=self.merchant, wine_vintage=self.wine_vintage, minimum_purchase_unit=1,
            url=url,
        )
        apply_update(WineData(id=id, product_url=url))
        wine = MerchantWine.objects.get(pk=wine.pk)
        self.assertEqual(id, wine.external_id)

    def test_change_product_url(self):
        id = 'test_change_product_url_id'
        url = 'test_change_product_url'
        wine = MerchantWine.objects.create(
            merchant=self.merchant, wine_vintage=self.wine_vintage, minimum_purchase_unit=1,
            external_id=id, url=url, available=False,
        )
        self.assertEqual((wine, []), apply_update(WineData(id=id, product_url=url)))

        update_url = 'url_changed'
        self.assertNotEqual((wine, []), apply_update(WineData(id=id, product_url=update_url)))
        self.assertEqual(update_url, MerchantWine.objects.get(pk=wine.pk).url)

    def test_allow_changing_external_id(self):
        id = 'test_allow_changing_external_id'
        apply_update(WineData(id=id, product_url=self.merchant_wine.url))
        wine = MerchantWine.objects.get(pk=self.merchant_wine.pk)
        self.assertEqual(id, wine.external_id)

    def test_set_available(self):
        id = 'test_set_available'
        wine = MerchantWine.objects.create(
            merchant=self.merchant, wine_vintage=self.wine_vintage, minimum_purchase_unit=1,
            available=False, external_id=id,
        )
        self.assertEqual((wine, []), apply_update(WineData(id=id)))
        self.assertFalse(MerchantWine.objects.get(pk=wine.pk).available)
        self.assertEqual((wine, []), apply_update(WineData(id=id, stock_availability='0')))
        self.assertFalse(MerchantWine.objects.get(pk=wine.pk).available)

        # set some stock and confirm changed
        self.assertNotEqual((wine, []), apply_update(WineData(id=id, stock_availability='10')))
        self.assertTrue(MerchantWine.objects.get(pk=wine.pk).available)
        self.assertEqual((wine, []), apply_update(WineData(id=id, stock_availability='20')))
        self.assertTrue(MerchantWine.objects.get(pk=wine.pk).available)

        # set back and confirm changed again
        self.assertNotEqual((wine, []), apply_update(WineData(id=id, stock_availability='0')))
        self.assertFalse(MerchantWine.objects.get(pk=wine.pk).available)

    def test_change_price(self):
        id = 'test_change_price_id'
        wine = MerchantWine.objects.create(
            merchant=self.merchant, wine_vintage=self.wine_vintage, minimum_purchase_unit=1,
            external_id=id, price=Decimal(100.0), available=False,
        )
        self.assertEqual((wine, []), apply_update(WineData(id=id, price='100')))

        updated_price = '200'
        self.assertNotEqual((wine, []), apply_update(WineData(id=id, price=updated_price)))
        self.assertEqual(Decimal(updated_price), MerchantWine.objects.get(pk=wine.pk).price)



    @skip('Comment out the decorator to run this test.')
    def test_print_results(self):
        update_all(debug=True)
