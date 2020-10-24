#Import modules
import requests
import os

#fetching data from yelp location API
yelp_url = 'https://api.yelp.com/v3/businesses/search'

#Get the key from the environment varialble

# print(YELP_API_KEY)

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
            # print(response)
            restaurants = response['businesses'] #results is a list
            # print(restaurants)

                # for r in restaurants:
                #     name = r['name']
                #     rating = r['rating']
                #     location = r['location']
                #     address =  ','.join(location['display_address'])
                
                #     print(f'{name}, {rating}, {address}')
            return restaurants
        
        except AssertionError as e:
            print('Requests.get() function was not executed')


    
