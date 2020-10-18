#Import modules
import requests
import os

#fetching data from yelp location API
yelp_url = 'https://api.yelp.com/v3/businesses/search'

#Get the key from the environment varialbles
YELP_API_KEY = os.environ.get('YELP_API_KEY')

def get_restaurants_for_location(location):
    
    headers = {'Authorization': 'Bearer %s' % YELP_API_KEY}
    query_params =  {'term': YELP_API_KEY, 'businesses': location}

        if query_params == 'term' and query_params == 'businesses':
            print('Found')
        else:
            print('Not found') 
    
    #Make a request to the yelp API
    #Convert JSON response to Python dictionary
    response = requests.get(yelp_url, params=query_params, headers=headers).json()
    print(response)

    restaurants = response['businesses'] #results is a list 

    for rs in restaurants:
        name = rs['name']
        rating = rs['rating']
        location = rs['location']
        address =  ','.join(location['display_address'])

        print(f'{name}, {rating}, {address}')


if __name__ == '__main__':
    restaurants = get_restaurants_for_location('Montana, MT') # change to different locations as needed 
    print(restaurants)
