import mysql.connector
import json

##### create MySQL table : attractions #####
sitedb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sontforg123",
  database="taipeiDayTrip"
)

cursor = sitedb.cursor()

cursor.execute('''CREATE TABLE attractions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255),
    description TEXT,
    address TEXT,
    transport TEXT,
    mrt VARCHAR(255),
    latitude VARCHAR(50),
    longitude VARCHAR(50),
    images TEXT)''')


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
    sql = "INSERT INTO attractions (name,category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, category, description, address, transport, mrt,latitude, longitude, images)
    cursor.execute(sql, val)
    sitedb.commit()
       

