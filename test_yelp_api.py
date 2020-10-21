import unittest
from unittest import TestCase
from unittest.mock import patch

import yelp_api

class TestYelpApi(unittest.TestCase):

    def test_get_search_location(self):
        self.assertEqual('', yelp_api.get_restaurants_for_location('term','location'))# test empty string
        self.assertEqual('Chicago', yelp_api.get_restaurants_for_location('      Chicago     '))# test for extra spaces

    @patch('yelp_api.get_restaurants_for_location', return_value='nowhere')
    def test_get_no_restaurants_for_location(self, mock_get_restaurants_for_location):
        yelp_api.zero_restaurants('', Minneapolis)
        mock_get_restaurants_for_location.assert_showed()

if __name__ == "__main__":
     unittest.main()        