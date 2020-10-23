#Import modules
import requests
import os

#fetching data from yelp location API
yelp_url = 'https://api.yelp.com/v3/businesses/search'

#Get the key from the environment varialble

YELP_API_KEY = os.environ.get('YELP_API_KEY')
# print(YELP_API_KEY)

def get_restaurants_for_location(location):
    YELP_API_KEY = 'zwNR-_GO-ShcVj2Gc9RheHSCG4rIitXhhm5juTyEGBFExzJzxqebyhcy6wQbkMSxAO-sUzLO3RO88c86jqTn87v7Q5e4X8XgNY7Abn2-B8SK3jwFg8d9LXllPdeBX3Yx'
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

                # for r in restaurants:
                #     name = r['name']
                #     rating = r['rating']
                #     location = r['location']
                #     address =  ','.join(location['display_address'])
                
                #     print(f'{name}, {rating}, {address}')
            return restaurants
        
        except  Exception as e:
            print('Requests.get() function was not executed', e)

if __name__ == '__main__':
    restaurants = get_restaurants_for_location('New York City, NY') # change to different locations as needed
    print(restaurants)

    
