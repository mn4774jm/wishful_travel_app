#TODO exception handling for data returned from wiki api
#TODO call to db to check for previous entry before consulting the api
#TODO when no data is found from wiki api, 'extract' is the only thing returned.
#TODO urls for restaurants are available in the yelp json data. If there is time consider working links in.

from states import state_list
from API.wiki_api import get_city_info, get_page_url
from API.yelp_api import get_restaurants_for_location
from API.ors_api import get_general_location_coordinates, get_directions
from flask import Blueprint, render_template, request
from flask_site.db import get_db
from helper_functions import restaurant_formatter, direction_formatting, get_coords
from db_calls import search_for_city_in_cache, add_to_cached_data

# Blueprint is used by __init__.py to import the page renderings into the app
# Also used to set up the url
bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        # request.form is a type of dict mapping
        city = request.form['city'].title()
        state = request.form['state']
        db = get_db()
        error = None

        if not city:
            error = 'City is required'
        elif not state:
            error = 'State is required'

        if error is None:

            cache_data = search_for_city_in_cache(city)
            if cache_data is None:
                page_id, page_data = get_city_info(city, state)
                add_to_cached_data()
                session_url = get_page_url(page_id)
                posts = get_restaurants_for_location(f'{city},{state}')
                data = get_coords(posts)
                res_list = restaurant_formatter(posts)
                end = get_general_location_coordinates(state,city)
                route = get_directions(data)
                directions = direction_formatting(route)


                if page_id is not False and posts is not None and end is not None:
                    # perfect world rendering. Runs when data is returned correctly.
                    return render_template('home/search.html', states=state_list, posts=page_data.split(), city_name=city, state_name=f', {state}',
                                           hyperlink=session_url, hypertitle='More Info', food=res_list,
                                           res_banner='Top Rated Restaurants', dir_banner='Driving Directions', routes=directions)

                else:
                    # rendering of page when an error occurs in one of the api calls. reports error message to user
                    return render_template('home/search.html', states=state_list, posts=f'{page_data}'.split())
            else:
                pass


    # works as the base rendering for the page. Only shows the submission fields.
    return render_template('home/search.html', states=state_list)
