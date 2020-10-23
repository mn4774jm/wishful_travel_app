import unittest
from unittest import TestCase
from unittest.mock import patch
import y_db


class TestYelpApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        y_db = os.path.join('database', 'test_yelp.db')
        YelpApi.instance = None

    def setUp(self):
        self.YA = YelpApi()
        self.clear_yelp_api()

    def test_get_search_location(self):
        self.assertEqual('', location.yelp_api(''))# test empty string
        self.assertEqual('Chicago', location.yelp_api('      Chicago     '))# test for extra spaces

    @patch('yelp_api.get_restaurants_for_location', return_value='nowhere')
    def test_get_no_restaurants_for_location(self, mock_get_restaurants_for_location):
        yelp_api.zero_restaurants('', Minneapolis)
        mock_get_restaurants_for_location.assert_showed()

if __name__ == "__main__":
     unittest.main()        