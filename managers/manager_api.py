from states import state_list
from API.wiki_api import get_city_info, refine_city_info, get_page_url
from API.yelp_api import get_restaurants_for_location
from API.ors_api import get_general_location_coordinates, get_directions
from flask import render_template
from utility_functions import restaurant_formatter, direction_formatting, get_coords
from db_calls import add_to_cached_data
import json


def api_manager(city, state):

    error, api_data = get_city_info(city, state)
    
    if error:
        return render_template('home/search.html', states=state_list, posts=f'{error}'.split())
    else:
        error, refined_data = refine_city_info(api_data)
        if error:
            return render_template('home/search.html', states=state_list, posts=f'{error}'.split())
        else:
            page_id = refined_data.page_id
            page_data = refined_data.intro_extract
            formatted_wiki_data = json.dumps(api_data)

            add_to_cached_data('wiki', city, formatted_wiki_data)

            error, session_url = get_page_url(page_id)
            if error:
                return render_template('home/search.html', states=state_list, posts=f'{error}'.split())
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