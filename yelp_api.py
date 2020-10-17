#Import modules
import os
import requests

feedback = ''

def get_user_feedback(): 
    #checking user input
    try:
        while not feedback:    
            feedback = input('What type of restaurants? ')
            print(feedback)
    except Exception as e:
        print('User entered incorrected information', e)

#fetching data from yelp location API
yelp_url = 'https://api.yelp.com/v3/businesses/search'
YELP_API_KEY = os.environ.get('YELP_API_KEY')
headers = {'Authorization': 'Bearer' + YELP_API_KEY}
parameters = {
    'term' : feedback,
    'categories' : 'restaurants',
    'location': 'Chicago,IL',
    'radius': '20000',
    'limit': 50}  

#Make a request to the yelp API
response = requests.get(yelp_url, headers=headers, params=parameters).json()
resturants = response['businesses']

for rs in resturants:
    name = rs['name']
    rating = rs['rating']
    location = rs['location']
    address =  ','.join(location['display_address'])

    print(f'{name}, {rating}, {address}')