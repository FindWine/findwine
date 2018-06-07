import os
from django.test import SimpleTestCase

from integrations.cybercellar import get_cybercellar_data


class CyberCellarFeedTest(SimpleTestCase):

    def test_parse_feed(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'cybercellar-feed.xml')) as f:
            raw_feed = f.read()

        data = list(get_cybercellar_data(raw_feed))

        self.assertEqual(3, len(data))
        wine_info = data[0]
        self.assertEqual('11588', wine_info.id)
        self.assertEqual('Billecart Salmon Brut Reserve', wine_info.name)
        self.assertEqual('https://www.cybercellar.com/billecart-salmon-brut-reserve',
                         wine_info.url)
        self.assertEqual('5', wine_info.stock_amount)
        self.assertEqual('746.00', wine_info.price)
