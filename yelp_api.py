#Import modules
import os
import requests

YELP_API_KEY = os.environ.get('YELP_API_KEY')

#fetching data from yelp location API
yelp_url = 'https://api.yelp.com/v3/businesses/search'

inquiry = input('What type of resturants? ')

#Define the Header

headers = {'Authorization': 'Bearer' + YELP_API_KEY}
parameters = {
    'term' : inquiry,
    'categories' : 'resturants',
    'location': 'Chicago,IL',
    'radius': '20000',
    'limit': 50}  
#Make a request to the yelp API
response = requests.get(yelp_url, headers=headers, params=parameters).json(0)
resturants = response['businesses']

for rs in resturants:
    name = rs['name']
    rating = rs['rating']
    location = rs['location']
    address =  ','.join(location['display_address'])

    print(f'{name}, {rating}, {address}')