from flask import Blueprint, render_template, request
from db_calls import get_bookmark_by_name
from managers.manager_bookmark import get_bookmark
bp = Blueprint('bookmarks', __name__, url_prefix='/bookmarks')


@bp.route('/marks', methods=('GET', 'POST'))
def get_bookmarks():
    place_list = get_bookmark_by_name()
    if request.method == 'POST':
        city = request.form['bookmark'].title()
        error = None
        if not city:
            error = 'City is required'

        if error is None:
            state, wiki, url, res_list, directions = get_bookmark(city)
            return render_template('favorites/bookmarks.html', books=place_list, wiki=wiki, city=city, state=f', {state}',
                                   hyperlink=url, hypertitle='More Info', food=res_list, res_banner='Top Rated Restaurants',
                                   dir_banner='Driving Directions', routes=directions)

    return render_template('favorites/bookmarks.html', books=place_list)
