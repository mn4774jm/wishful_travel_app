import requests
import logging
from dataclasses import dataclass

"""
Wiki API requests

get_city_info takes city and state arguments, attempts to contact the API,
and attempt to return the city's wikipedia page ID and the page introduction section.

get_page_url will use that returned page ID and shouldn't have any user input,
it will attempt to return only the page URL to be displayed for the User.

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

    try:
        data = requests.get(url, params=query).json()
        return None, data
    except ValueError as err:
        logging.error(f'JSON response error: {err}')
        return 'Wikipedia did not return an appropriate JSON response', None


def refine_city_info(data):
    page_data = data['query']['pages']
    page_id = list(page_data.keys())[0]

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


# def get_city_info(city, state):
#     query = {'action': 'query', 'format': 'json', 'titles': f'{city},_{state}', 'prop': 'extracts', 'exintro': '', 'explaintext': '', 'redirects': ''}
#     url = 'https://en.wikipedia.org/w/api.php?'

#     try:
#         data = requests.get(url, params=query).json()
#         page_data = data['query']['pages']
#         page_id = list(page_data.keys())
#         formatted_for_db_entry = json.dumps(data)
#         return page_id[0], page_data[f'{page_id[0]}']['extract'], formatted_for_db_entry
#     except KeyError as err:
#         return 'KeyError', err
#     except requests.exceptions.ConnectionError as err:
#         return 'ConnectionError', err


# def get_page_url(page_id):
#     query = {'action': 'query', 'prop': 'info', 'pageids': f'{page_id}', 'inprop': 'url', 'format': 'json'}
#     url = 'https://en.wikipedia.org/w/api.php?'

#     try:
#         data = requests.get(url, params=query).json()
#         return (data['query']['pages'][f'{page_id}']['fullurl'])
#     except KeyError as err:
#         return False


