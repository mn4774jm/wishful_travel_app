from states import state_list
from API.wiki_api import get_city_info, refine_city_info, get_page_url
from API.yelp_api import get_restaurants_for_location
from API.ors_api import get_general_location_coordinates, get_directions
from flask import render_template
from utility_functions import restaurant_formatter, direction_formatting, get_coords
from db_calls import add_to_cached_data
import json

# (page_id, posts, end, page_data, formatted_yelp_data, formatted_ors_data, session_url, res_list, directions)

def api_manager(city, state):

    api_error, api_data = get_city_info(city, state)
    
    if api_error:
        return (None, None, None, api_error, None, None, None, None, None)
    else:
        refine_error, refined_data = refine_city_info(api_data)
        if refine_error:
            return (None, None, None, refine_error, None, None, None, None, None)
        else:
            page_id = refined_data.page_id
            page_data = refined_data.intro_extract
            formatted_wiki_data = json.dumps(api_data)

            add_to_cached_data('wiki', city, formatted_wiki_data)

            url_error, session_url = get_page_url(page_id)
            if url_error:
                return (None, None, None, url_error, None, None, None, None, None)
            else:
                posts, formatted_yelp_data = get_restaurants_for_location(f'{city},{state}')
                add_to_cached_data('yelp', city, formatted_yelp_data)
                res_list = restaurant_formatter(posts)
                data = get_coords(posts)
                end = get_general_location_coordinates(state, city)
                route, formatted_ors_data = get_directions(data)
                add_to_cached_data('ors', city, formatted_ors_data)
                directions = direction_formatting(route)

                return page_id, posts, end, page_data, formatted_yelp_data, formatted_ors_data, session_url, res_list, directions