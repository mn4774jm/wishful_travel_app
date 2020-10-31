from API.wiki_api import get_city_info, refine_city_info, get_page_url
from API.yelp_api import get_restaurants_for_location
from API.ors_api import get_directions
from utility_functions import restaurant_formatter, direction_formatting, get_coords
from db_calls import add_to_cached_data
import json


def api_manager(city, state):

    api_error, api_data = get_city_info(city, state)
    
    if api_error:
        return (None, None, None, api_error, None, None, None, None)
    else:
        refine_error, refined_data = refine_city_info(api_data)
        if refine_error:
            return (None, None, None, refine_error, None, None, None, None)
        else:
            page_id = refined_data.page_id
            page_data = refined_data.intro_extract
            formatted_wiki_data = json.dumps(api_data)

            add_to_cached_data('wiki', city, state, formatted_wiki_data)

            url_error, session_url = get_page_url(page_id)
            if url_error:
                return (None, None, None, url_error, None, None, None, None)
            else:
                # data is collected from the yelp api and added into the cache via add_to_cache function
                posts, formatted_yelp_data = get_restaurants_for_location(f'{city},{state}')
                add_to_cached_data('yelp', city, state, formatted_yelp_data)
                # Data is formatted for easier reading when rendered in home.py
                res_list = restaurant_formatter(posts)
                # GPS coordinates are pulled from yelp json to be used for accurate directions when used with the ors
                # API.
                data = get_coords(posts)
                # end = get_general_location_coordinates(state, city)
                route, formatted_ors_data = get_directions(data)
                add_to_cached_data('ors', city, state, formatted_ors_data)
                directions = direction_formatting(route)

                return page_id, posts, page_data, formatted_yelp_data, formatted_ors_data, session_url, res_list, directions