from django.test import SimpleTestCase
from integrations.data_cleanup import url_is_valid


class DataCleanupTest(SimpleTestCase):
    # todo: convert to mock requests
    # https://stackoverflow.com/questions/15753390/python-mock-requests-and-the-response/28507806#28507806

    def test_url_valid(self):
        self.assertTrue(url_is_valid('https://www.google.com'))

    def test_url_invalid(self):
        self.assertFalse(url_is_valid('http://www.coryzue.com/404'))
