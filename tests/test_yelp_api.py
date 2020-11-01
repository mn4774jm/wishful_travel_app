import unittest
from unittest import TestCase
from unittest.mock import patch
from API import yelp_api #file to test


class YelpapiTest(unittest.TestCase):

    
    # def test_get_location(self): #Testing  get restaurants() in retrieving location    
    #     #Arrange
    #     print("Test 1: ")
    #     #Action
    #     result = yelp_api.get_restaurants_for_location('Minneapolis, MN')
    #     #Assert
    #     print(result)
    #     self.assertIsNotNone(result, None)
    
    """Checking yelp api for no restaurants"""
    
    @patch('requests.Response.json',return_value= {'error': {'code': 'LOCATION_NOT_FOUND', 'description':'Could not execute search, try specifying a more exact location.'}})
    def test_get_no_restaurants_for_location(self, mock_get_restaurants_for_location):
        no_restaurants = yelp_api.get_restaurants_for_location('')
        no_results = ''
        print(no_restaurants, no_results)
        #self.assertEqual(no_restaurants, msg = 'Search not found')
        self.assertEqual(no_restaurants, no_results )

    
    """Checking API server when it is not responding and flag exception for error code """

    @patch ('requests.Response.json', side_effect='Exception')   
    def test_api_when_error_in_connecting(self, mock_get_restaurants_for_location):
        try:
            actual = yelp_api.get_restaurants_for_location(location= None)
            err = 'the URL returned empty or blank data'
            if err == '':
                    print(err, msg = 'error code 505 and Service Unavailable')
            else:
                    print('API server is working.')
            expected = ''
            self.assertEqual(expected, actual)#AssertEqual() compares two parameters for same results
        except :
            print(Exception)
     

        



           