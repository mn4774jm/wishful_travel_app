import unittest
from unittest import TestCase

import yelp

class YelpapiTest(TestCase):

    def test_yelp_api_for_location(self):
        correct_location = yelp.restaurants_for_location('New York City', True)
        expected_location = 'Chicago'
        self.assertEqual(expected_location,correct_location)


if if __name__ == "__main__":
    unittest.main()        