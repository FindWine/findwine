import os
from django.test import SimpleTestCase
from integrations.port2port import get_port2port_data


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
        self.assertEqual('https://www.port2port.wine/buy-wine/arendsig/1000-vines-viognier-2016', wine_info.producturl)
        self.assertEqual('56', wine_info.stockavailability)
        self.assertEqual('150.00', wine_info.price)
        self.assertEqual('120', wine_info.deliverycost)
        self.assertEqual('ZAR', wine_info.currency)
