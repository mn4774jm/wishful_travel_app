from states import state_list
from API.wiki_api import get_city_info, get_page_url
from API.yelp_api import get_restaurants_for_location
from API.ors_api import get_general_location_coordinates, get_directions
from flask import render_template
from helper_functions import restaurant_formatter, direction_formatting, get_coords
from db_calls import add_to_cached_data

# this function will be renamed at a later date
def heavy_lifter(city, state):
    page_id, page_data, formatted_wiki_data = get_city_info(city, state)
    add_to_cached_data('wiki', city, formatted_wiki_data)

    if page_id == 'KeyError':
        return render_template('home/search.html', states=state_list, posts=f'The API was not able to retrieve information \
            on {city}, {state}.\nPlease check your spelling.'.split())
    elif page_id == 'ConnectionError':
        return render_template('home/search.html', states=state_list, posts=f'A network issue has occurred, \
            please check your connection.'.split())
    else:

        session_url = get_page_url(page_id)
        '''yelp'''
        posts, formatted_yelp_data = get_restaurants_for_location(f'{city},{state}')
        add_to_cached_data('yelp', city, formatted_yelp_data)
        res_list = restaurant_formatter(posts)
        '''ors'''
        data = get_coords(posts)
        end = get_general_location_coordinates(state, city)
        route, formatted_ors_data = get_directions(data)
        add_to_cached_data('ors', city, formatted_ors_data)
        directions = direction_formatting(route)
    return page_id, posts, end, page_data, formatted_yelp_data, formatted_ors_data, session_url, res_list, directions