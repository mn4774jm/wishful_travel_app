from flask import Blueprint, render_template, request
from db_calls import get_data_from_bookmarks, get_bookmark_by_name
from utility_functions import restaurant_formatter, convert_data_basic, direction_formatting
bp = Blueprint('bookmarks', __name__, url_prefix='/bookmarks')
import json

@bp.route('/marks', methods=('GET', 'POST'))
def get_bookmarks():
    place_list = get_bookmark_by_name()
    if request.method == 'POST':
        city = request.form['bookmark'].title()
        error = None
        if not city:
            error = 'City is required'

        if error is None:
            state = get_data_from_bookmarks('state', city)
            wiki = get_data_from_bookmarks('wiki_entry', city)
            url = get_data_from_bookmarks('wiki_url', city)
            res_list = restaurant_formatter(convert_data_basic(json.loads(get_data_from_bookmarks('restaurants', city))))
            directions = direction_formatting(convert_data_basic(json.loads(get_data_from_bookmarks('directions', city))))
            return render_template('favorites/bookmarks.html', books=place_list, wiki=wiki, city=city, state=f', {state}',
                                   hyperlink=url, hypertitle='More Info', food=res_list, res_banner='Top Rated Restaurants',
                                   dir_banner='Driving Directions', routes=directions)

    return render_template('favorites/bookmarks.html', books=place_list)
