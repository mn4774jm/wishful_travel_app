import sqlite3
from datetime import datetime
from db_config import db_path
import json
import time


# TODO exception handling and comments

# method to delete rows from the cache after a designated point in time. The expiry field in the cache table is the
# integer UTC value for the date the row was created plus 30 days. If that value is lower than the current, it is
# deleted
def check_expire_for_cache():
    with sqlite3.connect(db_path) as conn:
        dates_to_delete = conn.execute("DELETE FROM cache WHERE ? > expiry_date", (time.time(),))
        print(dates_to_delete)


# simple query to check if city already exists in the cache to avoid making api requests more than is required
def search_for_city_in_cache(city, state):
    with sqlite3.connect(db_path) as conn:
        data = conn.execute("SELECT * FROM cache WHERE city= ? and state = ?", (city, state))
        return data.fetchone()


# query to check if new row already exists in the DB before attempting to create a new row in the table
def search_bookmark_exists(city, state):
    with sqlite3.connect(db_path) as conn:
        data = conn.execute("SELECT * FROM bookmarks WHERE city= ? and state = ?", (city, state))
        return data.fetchone()


# data added to the new row includes an integer for UTC time plus an additional 30 days for the expiration date
def add_to_cached_data(api_name, city, state, data):
    with sqlite3.connect(db_path) as conn:
        conn.execute('insert into cache values (NULL,?,?, ?, ?,?)', (api_name, city, state, data, time.time() + 43200))
        conn.commit()


# TODO table not returning data when state argument is added to query
def get_data_from_cache(city, state, api):
    with sqlite3.connect(db_path) as conn:
        wiki_data = conn.execute("SELECT data FROM cache WHERE city= ? AND api_name= ?", (city, api))
        return wiki_data.fetchone()


def add_to_bookmarks(city, state, wiki_entry, restaurants, directions, wiki_url):
    with sqlite3.connect(db_path) as conn:
        try:
            conn.execute('insert into bookmarks values (NULL,?,?,?,?,?,?,?)',
                         (city, state, wiki_entry, restaurants, directions, wiki_url, datetime.now()))
            conn.commit()
        except ValueError as e:
            return 'Unable to commit to database'


def get_bookmark_by_name():
    book_names = []
    with sqlite3.connect(db_path) as conn:
        data = conn.execute("SELECT city FROM bookmarks")
        for row in data:
            data = json.loads(json.dumps(row))
            book_names.append(data[0])
            book_names.sort()
        return book_names


def get_data_from_bookmarks(field_type, city):
    with sqlite3.connect(db_path) as conn:
        data = conn.execute(f"SELECT {field_type} FROM bookmarks WHERE city = ?", (city,))
        for row in data:
            formatted = json.loads(json.dumps(row))
        return formatted[0]
