import unittest
from unittest import TestCase
from unittest.mock import patch

import requests
import yelp_api

class YelpapiTest(unittest.TestCase):

    def setUp(self):
        self.a = 'state'
        self.b = 'city'

         """ Testing  get restaurants() in retrieving location"""    
    def test_get_location(self):
        #Arrange
        print("Test 1: ")
        #Action
        result = requests.get(self.a, self.b)
        #Assert
        self.assertEqual(result, self.a, self.b)

             
    if __name__ == "__main__":
     unittest.main()            

        



           