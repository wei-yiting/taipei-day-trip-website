from model import db
from model.models import Attraction
import json


##### read-in and process DATA #####
with open('taipei-attractions.json', mode='r', encoding='utf-8') as file:
    data = file.read()
    json_data = json.loads(data)
    scene_list = json_data['result']['results']
    

##### insert values into table (row by row)#####
for scene in scene_list:
    name = scene['stitle']
    category = scene['CAT2']
    description = scene['xbody']
    address = scene['address']
    transport = scene['info']
    mrt = scene['MRT']
    latitude = scene['latitude']
    longitude = scene['longitude']
    files = scene['file'].split('http')
    
    images_string = ''
    for file in files:
        file_type = file[-3:]
        if file_type.lower() == 'jpg' or file_type.lower() == 'png':
            images_string += f'http{file},'
    images = images_string
    
    new_attraction = Attraction(name, category, description, address, transport, mrt, latitude, longitude, images)
    db.session.add(new_attraction)
    db.session.commit()
