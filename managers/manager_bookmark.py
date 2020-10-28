from utility_functions import convert_data_wiki
from db_calls import get_data_from_cache
from API.wiki_api import get_page_url
from db_calls import add_to_bookmarks
import json


def bookmark_manager(city, state):
    page_id, page_data = convert_data_wiki(get_data_from_cache(city, 'wiki'))
    session_url = get_page_url(page_id)
    formatted_yelp_data = get_data_from_cache(city, 'yelp')
    formatted_ors_data = get_data_from_cache(city, 'ors')
    add_to_bookmarks(city, str(state), page_data, json.dumps(formatted_yelp_data), json.dumps(formatted_ors_data),
                     session_url)




