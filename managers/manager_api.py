from states import state_list
from API.wiki_api import get_city_info, refine_city_info, get_page_url
from API.yelp_api import get_restaurants_for_location
from API.ors_api import get_general_location_coordinates, get_directions
from flask import render_template
from utility_functions import restaurant_formatter, direction_formatting, get_coords
from db_calls import add_to_cached_data
import json


def api_manager(city, state):

    api_error, api_data = get_city_info(city, state)
    # initial call to the wiki API, if an error is returned from this, then there's
    # no reason to run the other APIs, just returning the error.
    if api_error:
        return (None, None, None, api_error, None, None, None, None, None)
    else:
        # if there was a result (and this could still be an empty wiki response)
        # then it runs the next check to pull the page id and extract
        refine_error, refined_data = refine_city_info(api_data)
        if refine_error:
            return (None, None, None, refine_error, None, None, None, None, None)
        else:
            # if those came back right, then there's a wiki page for that city and state
            # and that info gets formatted to be added to the cache
            page_id = refined_data.page_id
            page_data = refined_data.intro_extract
            formatted_wiki_data = json.dumps(api_data)

            add_to_cached_data('wiki', city, formatted_wiki_data)
            # last check is for the url, used to make the link on the home page
            url_error, session_url = get_page_url(page_id)
            if url_error:
                return (None, None, None, url_error, None, None, None, None, None)
            else:
                # then the other APIs are run using that city state combo and formatted for the cache
                # the wiki API acting a bit like a validation check since there being a wiki page
                # is a good indicator that the city should exist for the other two
                # then all those responses can be passed back to the home.py page to be rendered
                posts, formatted_yelp_data = get_restaurants_for_location(f'{city},{state}')
                add_to_cached_data('yelp', city, formatted_yelp_data)
                res_list = restaurant_formatter(posts)
                data = get_coords(posts)
                end = get_general_location_coordinates(state, city)
                route, formatted_ors_data = get_directions(data)
                add_to_cached_data('ors', city, formatted_ors_data)
                directions = direction_formatting(route)

                return page_id, posts, end, page_data, formatted_yelp_data, formatted_ors_data, session_url, res_list, directions