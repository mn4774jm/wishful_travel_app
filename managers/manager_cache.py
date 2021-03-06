from utility_functions import convert_data_wiki, convert_data_basic
from db_calls import get_data_from_cache
from utility_functions import restaurant_formatter, direction_formatting
from API.wiki_api import get_page_url

# Cache manager is responsible for retrieving data from the cache to either be used to populate the renders or be
# added to the dictionary
def cache_manager(city, state):
    page_id, page_data = convert_data_wiki(get_data_from_cache(city, state, 'wiki'))
    session_url = get_page_url(page_id)
    res_list = restaurant_formatter(convert_data_basic(get_data_from_cache(city, state, 'yelp')))
    directions = direction_formatting(convert_data_basic(get_data_from_cache(city, state, 'ors')))
    return session_url, res_list, directions, page_id, page_data

