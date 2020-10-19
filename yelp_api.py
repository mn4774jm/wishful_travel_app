#Import modules
import requests
import os

#fetching data from yelp location API
yelp_url = 'https://api.yelp.com/v3/businesses/search'

#Get the key from the environment varialble
try:
    YELP_API_KEY = os.environ.get('YELP_API_KEY')
except KeyError:
    print("""
    An environment variable called YELP_API_KEY must be set containing the location
    of the yelp api key""")

def get_restaurants_for_location(term, location):
    
    headers = {'Authorization': 'Bearer %s' % YELP_API_KEY}
    query_params =  {'term': 'search_term','categories': category, 'location': location, 'radius': 10000, 'price': price, 'limit': 20}

    #if query_params == 'term' and query_params == 'businesses':
    #    print('Found')
    #else:
    #    print('Not found') 

    #Make a request to the yelp API
    #Convert JSON response to Python dictionary
    try:
            response = requests.get(yelp_url, params=query_params, headers=headers).json()
            print(response)

            restaurants = response['businesses'] #results is a list 

                for r in restaurants:
                name = r['name']
                rating = r['rating']
                location = r['location']
                address =  ','.join(location['display_address'])
            
                print(f'{name}, {rating}, {address}')

            return restaurants
    
    except AssertionError as e:
        print('Request.get() function was not executed')


if __name__ == '__main__':
    restaurants = get_restaurants_for_location('Minneapolis, MN) # change to different locations as needed 
    print(restaurants)
    
