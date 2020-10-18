import unittest
from unittest import TestCase

import location

class Testlocation(TestCase):

    def test_yelp_api_for_location(self):
        
        self.assertEqual('', location.yelp_api(''))# test empty string
        self.assertEqual('Chicago', location.yelp_api('      Chicago     '))# test for extra spaces

if __name__ == "__main__":
     unittest.main()        