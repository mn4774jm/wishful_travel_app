from unittest import TestCase
import yelp_api
import yelpdb.py
from unittest.mock import patch



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

    
    def test_add_location_duplicate_errors(self):
        lc = location('Minneapolis', 'Minneapol')
        lc.save()
        with self.assertRaises(LocationError):
                lc_dup = (location'Minneapolis', 'Minneapol')   
                lc_dup.save()

    @patch('yelp_api.get_restaurants_for_location', return_value='nowhere')
    def test_get_no_restaurants_for_location(self, mock_get_restaurants_for_location):
        yelp_a  pi.zero_restaurants('', Minneapolis)
        mock_get_restaurants_for_location.assert_showed()

if __name__ == "__main__":
     unittest.main()            

        

