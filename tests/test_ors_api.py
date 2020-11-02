import unittest
from unittest import TestCase
from unittest.mock import patch
from API import ors_api

# After the changes made to ors_api throughout development, the only module that now has a purpose in testing is get_directions
# On top of that, certain data doesn't need to be tested or caught because starting coordinates are predetermined (Minneapolis, MN)
# and destination coordinates are gathered from the Yelp api, which will only contain acceptable data.

# From what I can tell, I cannot create tests for except blocks other than what returns a KeyError, as everything else
# requires code in the ors_api.py file to be altered.

class TestOrsApi(TestCase):

    # Couldn't get mocking to work for ors_api yet.
    # @patch('ors_api.get_directions')
    # def test_acceptable_coordinates(self, mock_directions):
    #     mock_coordinates = '-80.1918, 25.7617' # Miami, Florida
    #     example_api_response = {"type":"FeatureCollection","features":[{"bbox":[8.681436,49.41461,8.69198,49.420514],"type":"Feature","properties":{"segments":[{"distance":1600.0,"duration":265.0,"steps":[{"distance":312.6,"duration":75.0,"type":11,"instruction":"Head north on Wielandtstraße","name":"Wielandtstraße","way_points":[0,10]},{"distance":737.1,"duration":106.1,"type":1,"instruction":"Turn right onto Mönchhofstraße","name":"Mönchhofstraße","way_points":[10,38]},{"distance":0.0,"duration":0.0,"type":10,"instruction":"Arrive at Roonstraße, straight ahead","name":"-","way_points":[61,61]}]}],"summary":{"distance":1600.0,"duration":265.0},"way_points":[0,61]},"geometry":{"coordinates":[[8.681496,49.41461],[8.68149,49.414711],[8.687872,49.420318]],"type":"LineString"}}],"bbox":[8.681436,49.41461,8.69198,49.420514],"metadata":{"attribution":"openrouteservice.org | OpenStreetMap contributors","service":"routing","timestamp":1604281567008,"query":{"coordinates":[[8.681495,49.41461],[8.687872,49.420318]],"profile":"driving-car","format":"json"},"engine":{"version":"6.3.0","build_date":"2020-09-21T01:00:26Z","graph_date":"1970-01-01T00:00:00Z"}}}
    
    # I'm not sure if it'll happen, but this is an example of if the location found
    # can't be reached exclusively by driving from Minneapolis, Minnesota
    def test_unavailable_directions(self):
        mock_coordinates = '-155.5828, 19.8968' # Hawaii (not a selectable state, this is purely an example)
        actual_error, actual_route = ors_api.get_directions(mock_coordinates)
        expected_error = 'Unable to create directions'
        self.assertEqual(expected_error, actual_error)
        self.assertIsNone(actual_route)

    # This is meant to receive 'Could not contact openrouteservice API'
    # Instead receives 'Unable to create directions'
    # However, receives the expected error if placed in ors_api. Why?
    def test_for_if_offline(self):
        mock_coordinates = '0, 0' # Doesn't matter, just needs to be something
        actual_error, actual_route = ors_api.get_directions(mock_coordinates)
        expected_error = 'Could not contact openrouteservice API'
        self.assertEqual(expected_error, actual_error)
        self.assertIsNone(actual_route)