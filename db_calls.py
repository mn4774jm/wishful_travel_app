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




