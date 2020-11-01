import requests
import os
import logging

"""

Uses openrouteservice API

Originally used experimental features from openrouteservice to fetch coordinates by the 'city, state' entered by the user,
but now has a preset starting point and uses coordnates pulled from Yelp for the endpoint, which is far more accurate.

All old code has been left to show my work and how the code changed over time, but has been commented out to easily show
what is still used.

"""

# ors_key = os.environ.get('ORS_API_KEY')
ors_key = '5b3ce3597851110001cf6248701a505f4a83471da001d266b2860ac6'
# country = 'usa'

# Uses coordinates for both the beginning and ending locations to retreive directions to travel from point A to point B.
def get_directions(end):

    # Catches error 403 if key is missing and if it's attempted to be obtained with an environment variable
    if ors_key is None:
        return 'Openrouteservice API key missing', None

    # parameter structure - key, start (long, lat), end (long, lat)
    directions_URL = ('https://api.openrouteservice.org/v2/directions/driving-car')

    start = '-93.278494, 44.941691'

    try:
        query_parameters = {'api_key': ors_key, 'start': start, 'end': end}

        try:
            query = requests.get(directions_URL, params=query_parameters).json()

        # Will likely catch more than error 503, but at least I can feel fairly confident that it'll catch error 503 
        # (can't specifically test for 503 because that would require the ors servers to be offline, but works when the user if offline)
        except:
            return 'Could not contact openrouteservice API', None

        steps = query['features'][0]['properties']['segments'][0]['steps']
        return None, steps

    # Catches error 400 and, if the key is incorrect, 403
    except KeyError:
        return 'Unable to create directions', None

    # Tried to catch error 503 here, but couldn't find any applicable code/keywords to use
    # Moved this try/except inside the first try block
    # except:
    #     return 'Could not contact openrouteservice API', None

    # Catches any miscellaneous errors that somehow got past the first two APIs
    except Exception as e:
        logging.error(e)
        return 'An unexpected error has been encountered', None

"""

# This method uses the Structured Forward Grocode Service to get the general area of whatever is being searched for, hopefully
# increasing search accuracy. The only data that gets retreived is what's in the coordinates field for the first element.
# def get_general_location_coordinates(state, city):

    # key, country, region (state), locality (city)
    structured_geosearch_URL = ('https://api.openrouteservice.org/geocode/search/structured')

    else:
        try:
            query_paramaters = {'api_key': ors_key, 'country': country, 'region': state, 'locality': city}
            query = requests.get(structured_geosearch_URL, params=query_paramaters).json()
            coordinates = query['features'][0]['geometry']['coordinates']
            return f'{str(coordinates[0])},{str(coordinates[1])}'

        except:
            print('Error: Location not found')

# Get hopefully more specific coordinates on a location, using coordinates obtained from the above method along with the entered place
# and state. If a combination of the two geosearches existed in ors, it would save a number of steps. Similar to above, the only
# retreived data is the coordinates, except it returns them sligntly formatted, to remove the brackets for use in getting directions.
# def get_location_coordinates(place, state, general_coordinates):

   # key, place + state, long, lat, country
   geosearch_URL = ('https://api.openrouteservice.org/geocode/search')

    try:
        # Location paramaters MUST be ordered from smallest to largest area and MUST be combined for the query to function
        combined_location_terms = f'{place} {state}'

        query_paramaters = {'api_key': ors_key, 'text': combined_location_terms, 'focus.point.lon': general_coordinates[0],
        'focus.point.lat': general_coordinates[1], 'boundary.country': country}

        query = requests.get(geosearch_URL, params=query_paramaters).json()
        coordinates = query['features'][0]['geometry']['coordinates']
        return f'{str(coordinates[0])},{str(coordinates[1])}'

    except:
        print('Error: Location not found')

Old for loop that was used to walk through each step of directions
count = 1
for s in steps:
    # Convert distances from meters to miles
    distance = round((s['distance']*3.28)/5280, 2)
    direction = s['instruction']
    print(f'{count}. {direction} | {distance} miles.')
    count += 1

Old code that was used to test the program while working on it
Now all that's needed is the endpoint (longitude, latitude) for get_directions

general_coordinates_1 = get_general_location_coordinates('minnesota', 'minneapolis')
print(general_coordinates_1)
general_coordinates_2 = get_general_location_coordinates('Wisconsin', 'Green bay')
print(get_directions(general_coordinates_1, general_coordinates_2))

general_coordinates_1 = get_general_location_coordinates('minnesota', 'minneapolis')
specific_coordinates_1 = get_location_coordinates('burger king', 'minnesota', general_coordinates_1)
print(specific_coordinates_1)

general_coordinates_1 = get_general_location_coordinates('minnesota', 'minneapolis')
specific_coordinates_1 = get_location_coordinates('burger king', 'minnesota', general_coordinates_1)

general_coordinates_2 = get_general_location_coordinates('minnesota', 'minneapolis')
specific_coordinates_2 = get_location_coordinates('mall of america', 'minnesota', general_coordinates_2)

get_directions(specific_coordinates_1, specific_coordinates_2)

"""