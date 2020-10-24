# # #TODO This is where calls to the DB should go
import sqlite3
from datetime import datetime
from db_config import db_path
#
def search_for_city_in_cache(city):
    with sqlite3.connect(db_path) as conn:
        # conn.row_factory = sqlite3.Row
        data = conn.execute("SELECT * FROM cache WHERE city= (?)", (city,))
        # conn.close()
        return data.fetchone()

def add_to_cached_data():
    with sqlite3.connect(db_path) as conn:
        conn.execute('insert into cache values (NULL,?,?,?,?)', )


# api_name = 'yelp'
# city = 'Minneapolis'
# data = 'I\'m json data!'
# # conn = sqlite3.connect(db_path)
# # conn.execute('insert into cache values (NULL, ?, ?, ?, ?)', (api_name, city, data, datetime.now()))
# # conn.commit()
# new_city = "Minneapolis"
# new_data = search_for_city_in_cache(city)
# for row in new_data:
#     print(row)
# print(new_data)
