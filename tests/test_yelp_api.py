import unittest
from unittest import TestCase
from unittest.mock import patch
import yelp
import requests

class YelpapiTest(unittest.TestCase):

    def setUp(self):
        self.a = 'state'
        self.b = 'city'
 
    def test_get_location(self): #Testing  get restaurants() in retrieving location    
        #Arrange
        print("Test 1: ")
        #Action
        result = requests.get(self.a, self.b)
        #Assert
        self.assertEqual(result, self.a, self.b)
    
    """Checking yelp api for no locations"""
    @patch('yelp_api.get_restaurants_for_location', return_value='nowhere')
    def test_get_no_restaurants_for_location(self, mock_get_restaurants_for_location):
        n_location = yelp.zero_restaurants('  ')
        mock_get_restaurants_for_location.assert_showed()
        print(n_location)
             
    if __name__ == "__main__":
     unittest.main()            

        



           