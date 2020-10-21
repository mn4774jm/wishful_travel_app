
def restaurant_formatter(posts):
    count = 0
    res_list = []
    for p in posts:
        count += 1
        temp_string = f'{count}. {p["name"]} || {p["categories"][0]["title"]} || Rating:{p["rating"]}'
        res_list.append(temp_string)
    return res_list
