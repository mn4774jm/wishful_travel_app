import unittest
from unittest import TestCase
from unittest.mock import patch

import requests
import yelp_api

class YelpapiTest(unittest.TestCase):

    def setUp(self):
        self.a = 'state'
        self.b = 'city'

    def test_get_location(self):
        #Arrange
        print("Test 1: ")
        #Action
        result = requests.get(self.a, self.b)
        #Assert
        self.assertEqual(result, self.a, self.b)


            """ Test get restaurants() in retrieving location"""       
    @patch('yelp_api.get_restaurants_for_location', return_value='nowhere')
    def test_get_no_restaurants_for_location(self, mock_get_restaurants_for_location):
        yelp_a  pi.zero_restaurants('', Minneapolis)
        mock_get_restaurants_for_location.assert_showed()

if __name__ == "__main__":
     unittest.main()            

        



           