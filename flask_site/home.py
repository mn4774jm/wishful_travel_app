from states import state_list
from flask import Blueprint, render_template, request
from db_calls import search_for_city_in_cache
from managers.manager_api import api_manager
from managers.manager_cache import cache_manager
from managers.manager_bookmark import bookmark_create, check_for_duplicate

# Blueprint is used by __init__.py to import the page renderings into the app
# Also used to set up the url
bp = Blueprint('home', __name__, url_prefix='/home')

# global variables are used so that both buttons can see the city and state needed for them to operate.
# I should be able to initialize them at the beginning of the search function, but so far no luck.
# the problem is that this a website with multiple customers. If I search for 'Anchorage' then city is 
# set to Anchorage. 
# in the meantime, someone else searches for 'Bentonville AK'. Now city is Bentonville.
# So now if I click Bookmark, city has been set to Bentonville so I'll get Bentonville saved, not Anchorage. 
# Generally avoid globals in web apps unless is something global to the application
# each route handler needs to be self-contained, a request should include all the data needed to 
# perform the request. 


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        # request.form is a type of dict mapping
        if request.form['submit_button'] == 'Search':
            city = request.form['city'].title()
            state = request.form['state']
            error = None
            if not city:
                error = 'City is required'
            elif not state:
                error = 'State is required'

            if error is None:
                cache_data = search_for_city_in_cache(city)
                if cache_data is None:

                    (page_id, posts, end, page_data, formatted_yelp_data, formatted_ors_data, session_url, res_list,
                     directions) = api_manager(city, state)

                    if page_id is not False and posts is not None and end is not None:

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
                    session_url, res_list, directions, page_id, page_data = cache_manager(city)
                    return render_template('home/search.html', states=state_list, posts=page_data.split(),
                                           hyperlink=session_url, hypertitle='More Info',
                                           city_name=city, state_name=f', {state}', food=res_list,
                                           res_banner='Top Rated Restaurants', dir_banner='Driving Directions',
                                           routes=directions)

        elif request.form['submit_button'] == 'Bookmark?':
            # this needs to figure out what the city is base on the request. 
            # the request should send the city and state
            print(request.form)  # generally avoid printing here - this is just to confirm the data is being set
            city = request.form['city']
            state = request.form['state']

            check = check_for_duplicate(city)
            if check is False:
                return render_template('home/search.html', message=f'{city} is already in your bookmarks', states=state_list)
            elif check is True:
                bookmark_create(city, state)
                return render_template('home/search.html', message=f'{city} saved to bookmarks!', states=state_list)

    # works as the base rendering for the page. Only shows the submission fields.
    return render_template('home/search.html', states=state_list)


