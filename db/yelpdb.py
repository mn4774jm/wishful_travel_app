import sqlite3
import yelp_api

db = 'yelp.DB_sqlite'
#create yelp database table 
def create_table():
    with sqlite3.connect(db) as conn: # connect to database
        conn.execute("""CREATE TABLE IF NOT EXISTS yelp
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        restaurant TEXT NOT NULL,
        name TEXT NOT NULL,
        rating INTEGER,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP) """)  
    conn.close()

#query database to look up information on specific places
def search_for_restaurants(name):
    error = None
    re = 'sushi'
    if re == 'sushi':
            with sqlite3.connect(db) as conn:
                cur = conn.cursor()
                try:
                    data = conn.execute("SELECT name FROM yelp WHERE name= ?", (name),)
                    cur.fetchall(data)    
                        #return conn.fetchall()
                    if data:
                        return data
                    else:
                        print("Invalid search. Try again.", error)
                except Exception as e:
                    return(e) 
            conn.close()        

    #Insert new city and state to yelp table
def insert_info(location):
     with sqlite3.connect(db) as conn:
         conn.execute("INSERT INTO yelp (id, city, state, restaurant, name, rating, created) VALUES (?, ? , ? , ?, ?, ?, ?", (
          location.id, location.city, location.state, location.restaurant, location.name, location.rating, location.created))
     
     conn.close()

    #Show all data by row in yelp table
def display_all_data():
    conn = sqlite3.connect(db)
    results = conn.execute('SELECT * FROM yelp')
    print('All data: ')
    for row in results:
        print(row)
    conn.close()

def display_one_location(location):
    conn = sqlite3.connect(db)
    results = conn.execute('SELECT FROM yelp WHERE restaurant like ?', (location,))   
    first_row = results.fetchone()
    if first_row:
        print('First row is: ', first_row)
    else:
        print('No search found')
    conn.close()

def add_new_restaurant():
    new_id = int(input('enter new id: '))
    new_name = input('enter new restaurant name: ')

    with sqlite3.connect(db) as conn:
        conn.execute(f'INSERT INTO products VALUES (?,?) ', (new_id, new_name))
    conn.close()

def update_restaurant():
    update_restaurant = 'Halloween Place'
    update_id = 500
   
    with sqlite3.connect(db) as conn:
        conn.execute('UPDATE yelp SET restaurant = ? WHERE id = ? '),
        (update_restaurant, update_id)

    conn.close()

def delete_state(state):
    with sqlite3.connect(db) as conn:
        conn.execute('DELETE from yelp WHERE name = ? ', (state, ) )
    conn.close()

create_table()
search_for_restaurants(name='sushi')
insert_info()
display_all_data()
display_one_location('Chicago')
add_new_restaurant()
update_restaurant()
delete_state('Maine')

          
          