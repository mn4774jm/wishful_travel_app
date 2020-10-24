import unittest
from unittest import TestCase

import yelp

class YelpapiTest(TestCase):

    def test_yelp_api_for_location(self):
        correct_location = yelp.restaurants_for_location('New York City', True)
        expected_location = 'Chicago'
        self.assertEqual(expected_location,correct_location)
import unittest
from unittest import TestCase
from unittest.mock import patch
import y_db


class TestYelpApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        y_db = os.path.join('database', 'test_yelp.db')
        location.instance = None

    def setUp(self):#Clear out database before and after testing
        self.YA = YelpApi()
        self.clear_yelp_api()

    def add_test_data(self):#Clear out yelp data
        self.clear_yelp_api()

        #set up data to test
        self.location1 = get_restaurants_for_location('Pizza', 'Chicago', True)
        self.location2 = get_restaurants_for_location('Dry Clean', 'New York City', True)

        #save data in database
        self.location1.save()
        self.location2.save()    

    def clear_yelp(self):
        self.YA.delete_all_locations()   

    def test_add_term_empty_location(self):
         lc = location('Chicag', 'Chicago')  
         lc.save()
         self.assertTrue(self.YA.exact_match(bk))#check for found location
         self.assertEqual(1, self.YA.location_count())  #Count 1 location found

    def test_add_location_duplicate_errors(self):
        lc = location('Minneapolis', 'Minneapol')
        lc.save()
        with self.assertRaises(LocationError):
                lc_dup = (location'Minneapolis', 'Minneapol')   
                lc_dup.save()

    # def test_get_search_location(self):
    #     self.assertEqual('', location.yelp_api(''))# test empty string
    #     self.assertEqual('Chicago', location.yelp_api('      Chicago     '))# test for extra spaces

    # @patch('yelp_api.get_restaurants_for_location', return_value='nowhere')
    # def test_get_no_restaurants_for_location(self, mock_get_restaurants_for_location):
    #     yelp_a  pi.zero_restaurants('', Minneapolis)
    #     mock_get_restaurants_for_location.assert_showed()

if __name__ == "__main__":
     unittest.main()            

        



           