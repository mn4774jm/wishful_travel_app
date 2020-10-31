import requests
import unittest
from unittest import TestCase
from unittest import mock
from API.wiki_api import get_city_info, refine_city_info, get_page_url

# figured out how to do patching request.get from here, or at least, learn a bit about it.
# https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response

def mock_requests_get(url, params):
    class MockAPI:
        def __init__(self, json_data):
            self.json_data = json_data
        
        def json(self):
            return self.json_data
    
    # returns mock JSON data depending on parameters in the request
    if params['prop'] == 'info':
        return MockAPI({"query":{"pages":{"6097240":{"title":"Minneapolis","fullurl":"https://en.wikipedia.org/wiki/Minneapolis"}}}})
    if params['titles'] == 'minneapolis,_mn':
        return MockAPI({"query":{"pages":{"6097240":{"pageid":6097240,"title":"Minneapolis","extract":"This is a correct API response"}}}})
    elif params['titles'] == 'test,_mn':
        return MockAPI({"query":{"pages":{"-1":{"title":"Test, MN","missing":""}}}})

    return MockAPI(None)

class TestWikiAPI(TestCase):

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_fetch_with_correct_city_name(self, mock_get):
        mock_response = {"query":{"pages":{"6097240":{"pageid":6097240,"title":"Minneapolis","extract":"This is a correct API response"}}}}
        error, data = get_city_info('minneapolis', 'mn')
        self.assertIsNone(error)
        self.assertEqual(mock_response, data)

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_fetch_with_incorrect_city_name(self, mock_get):
        mock_response = {"query":{"pages":{"-1":{"title":"Test, MN","missing":""}}}}
        error, data = get_city_info('test', 'mn')
        self.assertIsNone(error)
        self.assertEqual(mock_response, data)

    def test_refine_city_info_correct_city(self):
        mock_response = {"query":{"pages":{"6097240":{"pageid":6097240,"title":"Minneapolis","extract":"This is a correct API response"}}}}
        error, data = refine_city_info(mock_response)
        self.assertIsNone(error)
        self.assertEqual('6097240', data.page_id)

    def test_refine_city_info_incorrect_city(self):
        mock_response = {"query":{"pages":{"-1":{"title":"Test, MN","missing":""}}}}
        error, data = refine_city_info(mock_response)
        self.assertIsNotNone(error)
        self.assertIsNone(data)

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_fetch_wiki_page_full_url_correct_pageid(self, mock_get):
        mock_response = {"query":{"pages":{"6097240":{"title":"Minneapolis","fullurl":"https://en.wikipedia.org/wiki/Minneapolis"}}}}
        page_id = "6097240"
        error, url = get_page_url(page_id)
        self.assertIsNone(error)
        self.assertEqual("https://en.wikipedia.org/wiki/Minneapolis", url)

    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_fetch_wiki_page_full_url_forced_incorrect_pageid(self, mock_get):
        page_id = "-1"
        error, url = get_page_url(page_id)
        self.assertIsNone(url)
        self.assertEqual(error, "An invalid page ID was used, no request was made")
