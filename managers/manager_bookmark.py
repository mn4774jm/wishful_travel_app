from utility_functions import convert_data_wiki, convert_data_basic, restaurant_formatter, direction_formatting
from db_calls import get_data_from_cache, get_data_from_bookmarks
from API.wiki_api import get_page_url
from db_calls import add_to_bookmarks, search_bookmark_exists
import json


# Gets cache data for each of the api responses converts them to the appropriate datatype using json.dumps/loads,
# before committing them to the bookmarks table
def bookmark_create(city, state):
    page_id, page_data = convert_data_wiki(get_data_from_cache(city, state, 'wiki'))
    error, session_url = get_page_url(page_id)
    formatted_yelp_data = get_data_from_cache(city, state, 'yelp')
    formatted_ors_data = get_data_from_cache(city, state, 'ors')
    add_to_bookmarks(city, str(state), page_data, json.dumps(formatted_yelp_data), json.dumps(formatted_ors_data),
                     session_url)


# responsible for getting data from the bookmarks table and returning data to be rendered in bookmarks.py
def get_bookmark(city):
    state = get_data_from_bookmarks('state', city)
    wiki = get_data_from_bookmarks('wiki_entry', city)
    url = get_data_from_bookmarks('wiki_url', city)
    res_list = restaurant_formatter(convert_data_basic(json.loads(get_data_from_bookmarks('restaurants', city))))
    directions = direction_formatting(convert_data_basic(json.loads(get_data_from_bookmarks('directions', city))))
    return state, wiki, url, res_list, directions


# Checks the bookmarks table for a specific city/state before allowing the user to make a new entry in the bookmarks table
def check_for_duplicate(city, state):
    check = search_bookmark_exists(city, state)
    if check is None:
        return True
    else:
        return False

