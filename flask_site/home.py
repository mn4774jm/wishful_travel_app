from states import state_list

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_site.auth import login_required
from flask_site.db import get_db

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/search', methods=('GET', 'POST'))
def search():

    if request.method == 'POST':
        # request.form is a type of dict mapping
        username = request.form['city']
        password = request.form['state']
        db = get_db()
        error = None

    return render_template('home/search.html',states=state_list)
