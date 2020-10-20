from states import state_list
from wiki_api import get_city_info, get_page_url
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

    return render_template('home/dining.html', states=state_list, posts=posts.split())