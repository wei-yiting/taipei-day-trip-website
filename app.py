#from typing import Dict
from flask import *
import mysql.connector
import json

############################
######### set up  ##########
############################

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False


# connect to MySQL databases
sitedb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sontforg123",
  database="taipeiDayTrip"
)

cursor = sitedb.cursor()

############################
####### Pages view  ########
############################

@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


###############################
############# api #############
###############################

##### get attractions with 2 query : page and keyword #####
@app.route("/api/attractions")
def get_attractions():
    try:
        page = int(request.args.get('page'))
        keyword = request.args.get('keyword')
        
        if not keyword:
            cursor.execute('SELECT * FROM attractions')
            results = cursor.fetchall()
            
            page_count = cursor.rowcount // 12
            if page < page_count:
                next_page = page + 1
            else:
                next_page = None
            
            scene_list = []
            
            for result in results:
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
                
                scene_list.append(scene)
            
            start = page * 12
            end = (page + 1) * 12 
            response = {
				"nextPage": next_page,
				"data": scene_list[start:end]
			}
            
        else:
            keyword_query = f'SELECT * FROM attractions WHERE name LIKE "%{keyword}" OR category LIKE "%{keyword}%" OR description LIKE "%{keyword}%" OR address LIKE "%{keyword}%" OR mrt LIKE "%{keyword}%"'
            cursor.execute(keyword_query)
            results = cursor.fetchall()
            
            page_count = cursor.rowcount // 12
            if page < page_count:
                next_page = page + 1
            else:
                next_page = None
            
            scene_list = []
            for result in results:
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
                
                scene_list.append(scene)

            
            start = page * 12
            end = (page + 1) * 12 
            response = {
				"nextPage": next_page,
				"data": scene_list[start:end]
			}
        return make_response(jsonify(response),200)
    except:
        return make_response(jsonify({
			"error": True,
  			"message": "伺服器發生錯誤"
		}),500)
             

##### get single attraction by id #####
@app.route('/api/attraction/<attractionId>')
def get_attraction(attractionId):
    try:
        id_query = f'SELECT * FROM attractions WHERE id={attractionId}'
        cursor.execute(id_query)
        result = cursor.fetchone()
        if not result:
            return make_response(jsonify({"error":True,"message":"景點編號不正確"}),400)
        
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
        
        response = {
            "data": scene
        }
        return make_response(jsonify(response), 200)
    
    except:
        return make_response(jsonify({"error":True,"message": "伺服器內部出現錯誤"}),500)
app.run(port=3000,debug=True)


