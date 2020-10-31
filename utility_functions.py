import json


# function for human readable presentation conversion before being sent to the app
def restaurant_formatter(posts):
    count = 0
    res_list = []
    for p in posts:
        count += 1
        temp_string = f'{count}. {p["name"]} || {p["categories"][0]["title"]} || Rating:{p["rating"]}'
        res_list.append(temp_string)
    return res_list


# function for human readable presentation conversion before being sent to the app
def direction_formatting(steps):
    count = 1
    dir_list = []
    for s in steps:
        distance = round((s['distance'] * 3.28) / 5280, 2)
        print(distance)
        direction = s['instruction']
        print(direction)
        temp_string = f'{count}. {direction} | {distance} miles.'
        dir_list.append(temp_string)
        count += 1
    return dir_list


# gets coordinates from yelp api data for the first element in the restaurants list.
# This will be used by the ors api to get driving directions
def get_coords(posts):
    count = 0
    for p in posts:
        if count > 0:
            pass
        else:
            lat = p['coordinates']['latitude']
            lon = p['coordinates']['longitude']
            fixed_string = f'{lon},{lat}'
            count += 1
    return fixed_string

# Converts json data to string from tuple and into json. elements are then extracted and returned for use on the flask page
def convert_data_wiki(data):
    json_data = json.loads(json.dumps(data))
    refined_scope_data = json.loads(json_data[0])
    page_data = refined_scope_data['query']['pages']
    page_id = list(page_data.keys())
    return page_id[0], page_data[f'{page_id[0]}']['extract']


# converts data when retrieved from the cache to json data to be used in the app
def convert_data_basic(data):
    return json.loads(data[0])


# converts to string data so it can be stored in the bookmarks table
def convert_for_bookmarks_storage(data):
    return json.dumps(data)




