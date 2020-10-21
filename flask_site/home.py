from states import state_list
from API.wiki_api import get_city_info, get_page_url
from API.yelp_api import get_restaurants_for_location
from API.ors_api import get_general_location_coordinates, get_location_coordinates, get_directions
from flask import Blueprint, render_template, request
from flask_site.db import get_db

# Blueprint is used by __init__.py to import the page renderings into the app
# Also used to set up the url
bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/search', methods=('GET', 'POST'))
def search():

    if request.method == 'POST':
        # request.form is a type of dict mapping
        city = request.form['city']
        state = request.form['state']
        db = get_db()
        error = None

        if not city:
            error = 'City is required'
        elif not state:
            error = 'State is required'

        if error is None:
            #TODO exception handling for data returned from wiki api
            #TODO call to db to check for previous entry before consulting the api
            #TODO when no data is found from wiki api, 'extract' is the only thing returned.
            page_id, page_data = get_city_info(city, state)
            session_url = get_page_url(page_id)
            if page_id is not False:
                return render_template('home/search.html', states=state_list, posts=page_data.split(), city_name=city,
                                       hyperlink=session_url, hypertitle='More Info')
            else:
                return render_template('home/search.html', states=state_list, posts=f'{page_data}'.split())

    return render_template('home/search.html', states=state_list)


@bp.route('/dining', methods=('GET', 'POST'))
def dining():

    res_list = []
    if request.method == 'POST':
        # request.form is a type of dict mapping
        city = request.form['city']
        state = request.form['state']
        category = request.form['term']
        db = get_db()
        error = None

        if not city:
            error = 'City is required'
        elif not state:
            error = 'State is required'
        elif not category:
            error = 'Search term is required'

        if error is None:
            posts = get_restaurants_for_location(f'{city},{state}')

            count = 0
            for p in posts:
                count += 1
                temp_string = f'{count}. {p["name"]} || {p["categories"][0]["title"]} || Rating:{p["rating"]}'
                res_list.append(temp_string)

            return render_template('home/dining.html', states=state_list, posts=res_list)

    return render_template('home/dining.html', states=state_list, posts=res_list)


@bp.route('/directions', methods=('GET', 'POST'))
def directions():
    posts = ''
    if request.method == 'POST':
        # request.form is a type of dict mapping
        city = request.form['city']
        state = request.form['state']
        category = request.form['category']
        db = get_db()
        error = None

        if not city:
            error = 'City is required'
        elif not state:
            error = 'State is required'
        elif not category:
            error = 'Food type is required'

        if error is None:
            #TODO city and state information will need to be passed to the db to check for previous entries
            #TODO if a previous entry is found, data is pull from db and passed. Else, api is called for data
            posts = 'Data would go here; Can be split by section in html'

    return render_template('home/directions.html', states=state_list, posts=posts.split())