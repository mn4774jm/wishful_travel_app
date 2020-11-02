#Import modules
import requests
import os
import json

#fetching data from yelp location API
yelp_url = 'https://api.yelp.com/v3/businesses/search'

#Get the key from the environment varialble



def get_restaurants_for_location(location):
    
    YELP_API_KEY = os.environ.get('YELP_API_KEY')
    if YELP_API_KEY is None:
        print('No yelp api found')
    else:
        headers = {'Authorization': 'Bearer %s' % YELP_API_KEY}
        query_params =  {'categories': 'restaurants', 'location': location, 'rating':5, 'radius': 10000, 'limit': 10}
        
        #Make a request to the yelp API
        #Convert JSON response to Python dictionary
        try:
            response = requests.get(yelp_url, params=query_params, headers=headers).json()
            print(response)
            error = response['error']['code']
            if error == 'VALIDATION_ERROR':
                return 'Not valid information', None
            else:
                restaurants = response['businesses'] #results is a list
                formatted_for_db_entry = json.dumps(restaurants)
                return restaurants, formatted_for_db_entry 
            
        except AssertionError as e:
            print(e)

#print(get_restaurants_for_location("1245awertyu"))
print(get_restaurants_for_location(''))
    
