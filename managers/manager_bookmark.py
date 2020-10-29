from utility_functions import convert_data_wiki, convert_data_basic, restaurant_formatter, direction_formatting
from db_calls import get_data_from_cache, get_data_from_bookmarks
from API.wiki_api import get_page_url
from db_calls import add_to_bookmarks, search_bookmark_exists
import json


def bookmark_create(city, state):
    page_id, page_data = convert_data_wiki(get_data_from_cache(city, 'wiki'))
    session_url = get_page_url(page_id)
    formatted_yelp_data = get_data_from_cache(city, 'yelp')
    formatted_ors_data = get_data_from_cache(city, 'ors')
    add_to_bookmarks(city, str(state), page_data, json.dumps(formatted_yelp_data), json.dumps(formatted_ors_data),
                     session_url)


def get_bookmark(city):
    state = get_data_from_bookmarks('state', city)
    wiki = get_data_from_bookmarks('wiki_entry', city)
    url = get_data_from_bookmarks('wiki_url', city)
    res_list = restaurant_formatter(convert_data_basic(json.loads(get_data_from_bookmarks('restaurants', city))))
    directions = direction_formatting(convert_data_basic(json.loads(get_data_from_bookmarks('directions', city))))
    return state, wiki, url, res_list, directions


def check_for_duplicate(city):
    check = search_bookmark_exists(city)
    if check == None:
        return True
    else:
        return False

