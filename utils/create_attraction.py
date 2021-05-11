# reusable function for create scene data from database search result
def create_attraction_data(result):
    scene = {}
    scene['id'] = result[0]
    scene['name'] = result[1]
    scene['category'] = result[2]
    scene['description'] = result[3]
    scene['address'] = result[4]
    scene['transport'] = result[5]
    scene['mrt'] = result[6]
    scene['latitude'] = float(result[7])
    scene['longitude'] = float(result[8])
    scene['images'] = result[9].split(',')[:-1]
    return scene