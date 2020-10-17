#Import modules
import os
import requests

#fetching data from yelp location API
yelp_url = 'https://api.yelp.com/v3/businesses/search'

#Get the key from the environment varialbles
YELP_API_KEY = os.environ.get('YELP_API_KEY')

def get_restaurants_for_location(location):

    query_params =  {'access_key': YELP_API_KEY, 'businesses':location}
        if query_params:
            print(query_params)
        
        else:
            print('not found') 
    #Make a request to the yelp API
    #Convert JSON response to Python dictionary
    response = requests.get(yelp_url, params=query_params).json()

    print(response)

    resturants = response['businesses'] #results is a list 

    for rs in resturants:
        name = rs['name']
        rating = rs['rating']
        location = rs['location']
        address =  ','.join(location['display_address'])

        print(f'{name}, {rating}, {address}')


if __name__ == '__main__':
    restaurants = get_restaurants_for_location('Chicago,IL') # change to different locations as needed 
    print(restaurants)
