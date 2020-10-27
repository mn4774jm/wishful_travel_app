from states import state_list
from API.wiki_api import get_city_info, get_page_url
from API.yelp_api import get_restaurants_for_location
from API.ors_api import get_general_location_coordinates, get_directions
from flask import Blueprint, render_template, request
from flask_site.db import get_db
from helper_functions import restaurant_formatter, direction_formatting, get_coords, convert_data_wiki, convert_data_basic
from db_calls import search_for_city_in_cache, add_to_cached_data, get_data_from_cache, add_to_bookmarks

# Blueprint is used by __init__.py to import the page renderings into the app
# Also used to set up the url
bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        # request.form is a type of dict mapping
        # if request.form['submit_button'] == 'Search':
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
                '''wiki'''
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

                    if page_id is not False and posts is not None and end is not None:
                        add_to_bookmarks(city, state, page_data.split(), res_list, directions, session_url)
                        # perfect world rendering. Runs when data is returned correctly.
                        return render_template('home/search.html', states=state_list, posts=page_data.split(),
                                               city_name=city, state_name=f', {state}',
                                               hyperlink=session_url, hypertitle='More Info', food=res_list,
                                               res_banner='Top Rated Restaurants', dir_banner='Driving Directions',
                                               routes=directions)

                    else:
                        # rendering of page when an error occurs in one of the api calls. reports error message to user
                        return render_template('home/search.html', states=state_list, posts=f'{page_data}'.split())
            else:
                '''wiki'''
                page_id, page_data = convert_data_wiki(get_data_from_cache(city, 'wiki'))
                session_url = get_page_url(page_id)
                '''yelp'''
                res_list = restaurant_formatter(convert_data_basic(get_data_from_cache(city, 'yelp')))
                '''ors'''
                directions = direction_formatting(convert_data_basic(get_data_from_cache(city, 'ors')))
                return render_template('home/search.html', states=state_list, posts=page_data.split(),
                                       hyperlink=session_url, hypertitle='More Info',
                                       city_name=city, state_name=f', {state}', food=res_list,
                                       res_banner='Top Rated Restaurants', dir_banner='Driving Directions',
                                               routes=directions)

    # works as the base rendering for the page. Only shows the submission fields.
    return render_template('home/search.html', states=state_list)
