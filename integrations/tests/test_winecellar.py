import os
from django.test import SimpleTestCase

from integrations.winecellar import get_winecellar_data


class WineCellarFeedTest(SimpleTestCase):

    def test_parse_feed(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'winecellar-feed.xml')) as f:
            raw_feed = f.read()

        data = list(get_winecellar_data(raw_feed))
        self.assertEqual(3, len(data))
        wine_info = data[0]
        self.assertEqual('2752', wine_info.id)
        self.assertEqual('Boplaas Cape Tawny', wine_info.name)
        self.assertEqual('http://www.winecellar.co.za/boplaas-cape-tawny-nv.html',
                         wine_info.url)
        self.assertEqual('1', wine_info.stock_amount)
        self.assertEqual('140.00', wine_info.price)
