import requests
import os

"""

Uses openrouteservice API

Note 1 - Order as follows: structured_geosearch, geosearch, directions
Note 2 - Requests are sometimes inaccurate unless an exact address is given. Also, using the full spelling of the state sometimes helps.
Note 3 - If possible, maybe have Yelp API directly send info with a button to increase accuracy and improve user experience?
Note 4 - Special charatcers typically break things (not crashing, just bad data), so will need to add a way to prevent/remove them

"""

# key, country, region (state), locality (city)
structured_geosearch_URL = ('https://api.openrouteservice.org/geocode/search/structured')

# key, place + state, long, lat, country
geosearch_URL = ('https://api.openrouteservice.org/geocode/search')

# key, start (long, lat), end (long, lat)
directions_URL = ('https://api.openrouteservice.org/v2/directions/driving-car')

# ors_key = os.environ.get('ORS_API_KEY')
ors_key = '5b3ce3597851110001cf6248701a505f4a83471da001d266b2860ac6'
country = 'usa'

# This method uses the Structured Forward Grocode Service to get the general area of whatever is being searched for, hopefully
# increasing search accuracy. The only data that gets retreived is what's in the coordinates field for the first element.
def get_general_location_coordinates(state, city):
    if ors_key is None:
        print('openrouteservice API key missing')

    else:
        try:
            query_paramaters = {'api_key': ors_key, 'country': country, 'region': state, 'locality': city}
            query = requests.get(structured_geosearch_URL, params=query_paramaters).json()
            coordinates = query['features'][0]['geometry']['coordinates']
            return f'{str(coordinates[0])},{str(coordinates[1])}'
        except:
            print('Error: Location not found')

# Get hopefully more specific coordinates on a location, using coordinates obtained from the above method along with the entered place
# and state. If a combination of the two geosearches existed in ors, it would saved a number of steps. Similar to above, the only
# retreived data is the coordinates, except it returns them sligntly formatted, to remove the brackets for use in getting directions.
# def get_location_coordinates(place, state, general_coordinates):
#     try:
#         # Location paramaters MUST be ordered from smallest to largest area and MUST be combined for the query to function
#         combined_location_terms = f'{place} {state}'
#
#         query_paramaters = {'api_key': ors_key, 'text': combined_location_terms, 'focus.point.lon': general_coordinates[0],
#         'focus.point.lat': general_coordinates[1], 'boundary.country': country}
#
#         query = requests.get(geosearch_URL, params=query_paramaters).json()
#         coordinates = query['features'][0]['geometry']['coordinates']
#         return f'{str(coordinates[0])},{str(coordinates[1])}'
#
#     except:
#         print('Error: Location not found')


# Uses coordinates for both the beginning and ending locations to retreive and display directions to travel from point A to point B.
def get_directions(end):
    start = '-93.278494,44.941691'
    try:
        query_parameters = {'api_key': ors_key, 'start': start, 'end': end}
        query = requests.get(directions_URL, params=query_parameters).json()
        steps = query['features'][0]['properties']['segments'][0]['steps']
        return steps

    except:
        print('Error: Unable to find path')
        return None
        # For loop to walk through each step of directions
        # count = 1
        # for s in steps:
        #     # Convert distances from meters to miles
        #     distance = round((s['distance']*3.28)/5280, 2)
        #     direction = s['instruction']
        #     print(f'{count}. {direction} | {distance} miles.')
        #     count += 1

# general_coordinates_1 = get_general_location_coordinates('minnesota', 'minneapolis')
# print(general_coordinates_1)
# general_coordinates_2 = get_general_location_coordinates('Wisconsin', 'Green bay')
# print(get_directions(general_coordinates_1, general_coordinates_2))

# general_coordinates_1 = get_general_location_coordinates('minnesota', 'minneapolis')
# specific_coordinates_1 = get_location_coordinates('burger king', 'minnesota', general_coordinates_1)
# print(specific_coordinates_1)


"""

Basic code used to test the program while working on it, feel free to plug in your own data


general_coordinates_1 = get_general_location_coordinates('minnesota', 'minneapolis')
specific_coordinates_1 = get_location_coordinates('burger king', 'minnesota', general_coordinates_1)

general_coordinates_2 = get_general_location_coordinates('minnesota', 'minneapolis')
specific_coordinates_2 = get_location_coordinates('mall of america', 'minnesota', general_coordinates_2)

get_directions(specific_coordinates_1, specific_coordinates_2)

"""
