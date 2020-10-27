# # #TODO This is where calls to the DB should go
import sqlite3
from datetime import datetime
from db_config import db_path


def search_for_city_in_cache(city):
    with sqlite3.connect(db_path) as conn:
        data = conn.execute("SELECT * FROM cache WHERE city= ?", (city,))
        return data.fetchone()


def add_to_cached_data(api_name, city, data):
    with sqlite3.connect(db_path) as conn:
        conn.execute('insert into cache values (NULL,?,?,?,?)', (api_name, city, data, datetime.now()))
        conn.commit()


def get_data_from_cache(city, api):
    with sqlite3.connect(db_path) as conn:
        wiki_data = conn.execute("SELECT data FROM cache WHERE city= ? AND api_name= ?", (city, api))
        return wiki_data.fetchone()


def add_to_bookmarks(city, state, wiki_entry, restaurants, directions, wiki_url):
    with sqlite3.connect(db_path) as conn:
        conn.execute('insert into bookmarks values (NULL,?,?,?,?,?,?,?)', (city, state, wiki_entry, restaurants, directions, wiki_url, datetime.now()))
        conn.commit()


def get_data_from_bookstore():
    pass




