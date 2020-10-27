import json
def restaurant_formatter(posts):
    count = 0
    res_list = []
    for p in posts:
        count += 1
        temp_string = f'{count}. {p["name"]} || {p["categories"][0]["title"]} || Rating:{p["rating"]}'
        res_list.append(temp_string)
    return res_list

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


def get_coords(posts):
    address = ''
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

def convert_data_wiki(data):
    '''wiki may need to be split into two functions.
     That way data pulled from the DB and be sent directly to through
     the function that sets up the data for the page.'''
    json_data = json.loads(json.dumps(data))
    refined_scope_data = json.loads(json_data[0])
    page_data = refined_scope_data['query']['pages']
    page_id = list(page_data.keys())
    return page_id[0], page_data[f'{page_id[0]}']['extract']


def convert_data_basic(data):
    return json.loads(data[0])





