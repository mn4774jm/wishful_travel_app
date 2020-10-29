import requests
import json
"""
Wiki API requests

get_city_info takes city and state arguments, attempts to contact the API,
and attempt to return the city's wikipedia page ID and the page introduction section.

get_page_url will use that returned page ID and shouldn't have any user input,
it will attempt to return only the page URL to be displayed for the User.

"""


def get_city_info(city, state):
    query = {'action': 'query', 'format': 'json', 'titles': f'{city},_{state}', 'prop': 'extracts', 'exintro': '', 'explaintext': '', 'redirects': ''}
    url = 'https://en.wikipedia.org/w/api.php?'

    try:
        data = requests.get(url, params=query).json()
        page_data = data['query']['pages']
        page_id = list(page_data.keys())
        formatted_for_db_entry = json.dumps(data)
        return page_id[0], page_data[f'{page_id[0]}']['extract'], formatted_for_db_entry
    except KeyError as err:
        return 'KeyError', err
    except requests.exceptions.ConnectionError as err:
        return 'ConnectionError', err


def get_page_url(page_id):
    query = {'action': 'query', 'prop': 'info', 'pageids': f'{page_id}', 'inprop': 'url', 'format': 'json'}
    url = 'https://en.wikipedia.org/w/api.php?'

    try:
        data = requests.get(url, params=query).json()
        return (data['query']['pages'][f'{page_id}']['fullurl'])
    except KeyError as err:
        return False


