from flask_site.static.states import state_list
from flask import Blueprint, render_template, request
from db_calls import search_for_city_in_cache, check_expire_for_cache
from managers.manager_api import api_manager
from managers.manager_cache import cache_manager
from managers.manager_bookmark import bookmark_create, check_for_duplicate

# Blueprint is used by __init__.py to import the page renderings into the app
# Also used to set up the url
bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/search', methods=('GET', 'POST'))
def search():

    if request.method == 'POST':
        # request.form is a type of dict mapping
        # listens for button push for the 'Search' button
        if request.form['submit_button'] == 'Search':
            #gets strings from search page for user entry to be passed to the apis
            city = request.form['city'].title()
            state = request.form['state']
            error = None
            # Check to make sure all fields are filled in
            if not city:
                error = 'City is required'
            elif not state:
                error = 'State is required'

            if error is None:
                # checks cache for previous entry as to not call the api more than necessary.
                check_expire_for_cache()
                cache_data = search_for_city_in_cache(city, state)
                if cache_data is None:
                    # Call to api manager to facilitate api requests to wiki, yelp, and openroutesource apis; returns
                    # data needed to render page

                    (page_id, posts, page_data, formatted_yelp_data, formatted_ors_data, session_url, res_list,
                     directions) = api_manager(city, state)
                    if page_data is None:
                        return render_template('home/search.html', states=state_list, message='No data found for location')
                    else:
                        if page_id is not False and posts is not None:

                            # perfect world rendering. Runs when data is returned correctly.
                            return render_template('home/search.html', states=state_list, posts=page_data.split(),
                                                   city_name=city, state_name=f', {state}',
                                                   hyperlink=session_url, hypertitle='More Info', food=res_list,
                                                   res_banner='Top Rated Restaurants', dir_banner='Driving Directions',
                                                   routes=directions)

                        else:
                            # rendering of page when an error occurs in one of the api calls. reports error message to user
                            return render_template('home/search.html', states=state_list, message=page_data)

                # If matching entry already exists in the cache data will be returned from the cache table for rendering
                else:
                    # call to manager to retrieve data from the cache
                    session_url, res_list, directions, page_id, page_data = cache_manager(city, state)
                    return render_template('home/search.html', states=state_list, posts=page_data.split(),
                                           hyperlink=session_url, hypertitle='More Info',
                                           city_name=city, state_name=f', {state}', food=res_list,
                                           res_banner='Top Rated Restaurants', dir_banner='Driving Directions',
                                           routes=directions)

        # button to bookmark page using most recent user filled fields
        elif request.form['submit_button'] == 'Bookmark?':
            error = None
            city = request.form['city']
            state = request.form['state']
            if not city:
                error = 'City is required'
            elif not state:
                error = 'State is required'

            if error is None:
                # call to check if data is already in the bookmarks table before attempting entry
                check = check_for_duplicate(city, state)
                # if data is already in bookmarks table, no new entry is attempted and the user is notified
                if check is False:
                    return render_template('home/search.html', message=f'{city} is already in your bookmarks', states=state_list)

                # If not in table, call to add new entry using data from the cache as opposed to another api call
                elif check is True:
                    bookmark_create(city, state)
                    return render_template('home/search.html', message=f'{city} saved to bookmarks!', states=state_list)

    # works as the base rendering for the page. Only shows the submission fields.
    return render_template('home/search.html', states=state_list)


