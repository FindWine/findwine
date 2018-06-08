import json
import os
from django.test import SimpleTestCase

from integrations.vinoteque import get_vinoteque_data, _get_quantity_and_size_from_variant_title, \
    _get_variant_to_use


class VinotequeFeedTest(SimpleTestCase):

    def test_parse_titles(self):
        test_cases = [
            ("1x750ml", 1, '750ml'),
            ("6x750ml", 6, '750ml'),
            ("6x750ml || Mature", 6, '750ml'),
            ("1x1.5L", 1, '1.5l'),
            ("12x750ml || Mature", 12, '750ml'),
            ("1x3L", 1, '3l'),
            ("6x375ml", 6, '375ml'),
            ("1x9L", 1, '9l'),
            ("1xGift Pack", 1, 'gift'),
            ("1X750ml", 1, '750ml'),
            ("6x1.5l || Mature", 6, '1.5l'),
        ]
        for test_case in test_cases:
            self.assertEqual((test_case[1], test_case[2]), _get_quantity_and_size_from_variant_title(test_case[0]))

    def notest_get_variant_to_use_available_first(self):
        v1 = {
          "id": 1,
          "title": "1x750ml",
          "available": False,
        }
        v2 = {
          "id": 2,
          "title": "1x750ml",
          "available": True,
        }
        self.assertEqual(2, _get_variant_to_use([v1, v2])['id'])

    def test_get_variant_to_use_by_quantity(self):
        q_1 = {
          "id": 1,
          "title": "1x750ml",
          "available": True,
        }
        q_6 = {
          "id": 2,
          "title": "6x750ml",
          "available": True,
        }
        q_12 = {
          "id": 3,
          "title": "12x750ml",
          "available": True,
        }
        self.assertEqual(1, _get_variant_to_use([q_1, q_6, q_12])['id'])
        self.assertEqual(1, _get_variant_to_use([q_6, q_1, q_12])['id'])
        self.assertEqual(2, _get_variant_to_use([q_6, q_12])['id'])
        self.assertEqual(2, _get_variant_to_use([q_12, q_6])['id'])

    def test_get_variant_to_use_by_size(self):
        size_750 = {
          "id": 1,
          "title": "1x750ml",
          "available": True,
        }
        size_15 = {
          "id": 2,
          "title": "6x1.5l",
          "available": True,
        }
        self.assertEqual(1, _get_variant_to_use([size_15, size_750])['id'])

    def test_quantity_trumps_size(self):
        v_6_750 = {
          "id": 1,
          "title": "6x750ml",
          "available": True,
        }
        v_1_5 = {
          "id": 2,
          "title": "1x1.5l",
          "available": True,
        }
        self.assertEqual(2, _get_variant_to_use([v_6_750, v_1_5])['id'])

    def test_availabilityf_trumps_quantity(self):
        v_1_750 = {
          "id": 1,
          "title": "6x750ml",
          "available": False,
        }
        v_6_755 = {
          "id": 2,
          "title": "6x750ml",
          "available": True,
        }
        self.assertEqual(2, _get_variant_to_use([v_1_750, v_6_755])['id'])

    def test_parse_feed(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'vinoteque-feed.json')) as f:
            raw_feed = json.loads(f.read())

        data = list(get_vinoteque_data(raw_feed))
        self.assertEqual(3, len(data))
        wine_info = data[0]
        self.assertEqual(1321042116683, wine_info.id)
        self.assertEqual('Plaisir de Merle Chardonnay 2017', wine_info.name)
        self.assertEqual('https://www.vinoteque.co.za/products/plaisir-de-merle-chardonnay-2017-750ml',
                         wine_info.url)
        self.assertEqual(1, wine_info.stock_amount)
        self.assertEqual('135.01', wine_info.price)

        # this implicitly tests some selection behavior as well as dividing the price
        # by six when necessary
        wine_info_by_six = data[1]
        self.assertEqual('162.00', wine_info_by_six.price)
