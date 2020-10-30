import unittest
from unittest import TestCase
from unittest.mock import patch
from API import yelp_api


class YelpapiTest(unittest.TestCase):

    def setUp(self):
        self.a = 'state'
        self.b = 'city'
 
    def test_get_location(self): #Testing  get restaurants() in retrieving location    
        #Arrange
        print("Test 1: ")
        #Action
        result = yelp_api.get_restaurants_for_location('Minneapolis, MN')
        #Assert
        print(result)
        self.assertIsNotNone(result, None)
    
    """Checking yelp api for no locations"""
    
    @patch('requests.Response.json',return_value= {'error': {'code': 'LOCATION_NOT_FOUND', 'description':'Could not execute search, try specifying a more exact location.'}})
    def test_get_no_restaurants_for_location(self, mock_get_restaurants_for_location):
        no_location = yelp_api.get_restaurants_for_location('Search not found')
        print(no_location)

    
    #Checking when API server is down
    @patch ('api.get_restaurants_for_location', side_effect=Exception())   
    def test_api_when_error_connecting(self, mock_request_get):
        l = yelp_api.get_restaurants_for_location('California, CA')
        print(l) 

if __name__ == "__main__":
     unittest.main()            

        



           