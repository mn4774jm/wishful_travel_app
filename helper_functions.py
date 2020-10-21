
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


