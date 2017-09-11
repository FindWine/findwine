from django.test import SimpleTestCase
from geoposition import Geoposition
from wine.geoposition import geoposition_to_dms_string


class GeopositionTest(SimpleTestCase):

    def test_simple(self):
        self.assertEqual('''S 33° 49' 20.92" E 18° 55' 48.51"''',
                         geoposition_to_dms_string(Geoposition(-33.8224777, 18.9301428)))

    def test_near_zero(self):
        self.assertEqual('''S 0° 49' 20.92" W 0° 55' 48.51"''',
                         geoposition_to_dms_string(Geoposition(-0.8224777, -0.9301428)))
        self.assertEqual('''N 0° 49' 20.92" E 0° 55' 48.51"''',
                         geoposition_to_dms_string(Geoposition(0.8224777, 0.9301428)))
