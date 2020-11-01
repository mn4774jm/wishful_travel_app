import requests
import logging
from dataclasses import dataclass

"""
Wiki API requests

get_city_info takes city and state arguments, attempts to contact the API,
and attempt to return the full json response (which is formatted later for the cache).

refine_city_info takes that json again and will dig into it to pull out the 
page ID and the intro extract for displaying.

get_page_url will use that returned page ID and shouldn't have any user input,
it will attempt to return value errors, or None and the page URL to be displayed for the User.

"""


@dataclass
class WikiApiResponse:
    page_id: str
    intro_extract: str


def get_city_info(city, state):

    query = {
        'action': 'query',
        'format': 'json',
        'titles': f'{city},_{state}',
        'prop': 'extracts',
        'exintro': '',
        'explaintext': '',
        'redirects': ''
    }

    url = 'https://en.wikipedia.org/w/api.php?'
    # Initial API info request, returning a dictionary even if the request didn't find 
    # a proper page on wikipedia as long as there isn't an error
    try:
        data = requests.get(url, params=query).json()
        return None, data
    except ValueError as err:
        logging.error(f'JSON response error: {err}')
        return None, 'Wikipedia did not return an appropriate JSON response'


def refine_city_info(data):
    # Once it's past the API, that request has to be refined, pulling out the pages data
    # which is necessary because the key needed to get the intro extract changes to that page number
    page_data = data['query']['pages']
    page_id = list(page_data.keys())[0]
    # if the request didn't find a city's wiki page, it'll return a -1 as the key
    # so any time this happens, there is no 'extract', so a key error is avoidable.
    # if it passes that, there's page info to extract, turn into a response, and send back
    if page_id == '-1':
        return 'No Wikipedia page found for this city, please check your spelling', None
    else:
        intro_extract = page_data[f'{page_id}']['extract']
        wiki_response = WikiApiResponse(page_id, intro_extract)
        return None, wiki_response


def get_page_url(page_id):

    query = {
        'action': 'query',
        'prop': 'info',
        'pageids': f'{page_id}',
        'inprop': 'url',
        'format': 'json'
    }

    url = 'https://en.wikipedia.org/w/api.php?'
    # getting the page url is really easy once we've extracted the page id required
    # and if the user manages to swap it with a -1, then it won't try to make the request
    # otherwise, the page id extracted from the wiki response itself will be used
    # so there's not user error. then the response is simple and the url can be grabbed as a string
    if page_id == '-1':
        return 'An invalid page ID was used, no request was made', None
    else:
        try:
            data = requests.get(url, params=query).json()
            page_url = data['query']['pages'][f'{page_id}']['fullurl']
            return (None, page_url)

        except ValueError as err:
            logging.error(f'JSON response error: {err}')
            return 'Wikipedia did not return an appropriate JSON response', None
