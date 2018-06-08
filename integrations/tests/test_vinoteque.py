import os
from django.test import SimpleTestCase

from integrations.vinoteque import get_vinoteque_data


class WineCellarFeedTest(SimpleTestCase):

    def test_parse_feed(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'vinoteque-feed.json')) as f:
            raw_feed = f.read()

        data = list(get_vinoteque_data(raw_feed))
        self.assertEqual(3, len(data))
        wine_info = data[0]
        self.assertEqual(1321042116683, wine_info.id)
        self.assertEqual('Plaisir de Merle Chardonnay 2017', wine_info.name)
        self.assertEqual('https://www.vinoteque.co.za/products/plaisir-de-merle-chardonnay-2017-750ml',
                         wine_info.url)
        self.assertEqual(1, wine_info.stock_amount)
        self.assertEqual('135.01', wine_info.price)
