from config import DbCfg
from flask import *
import mysql.connector
from mysql.connector import pooling

############################
######### set up  ##########
############################

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False


# connect to MySQL databases
connectionpool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name = 'MySQLPool',
        pool_size = 3,
        host = DbCfg.host,
        user = DbCfg.usr,
        password = DbCfg.pwd,
        database = DbCfg.db
 )

sitedb = connectionpool.get_connection()

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


##### attraction ######

# reusable function for create scene data from database search result
def create_scene_data(result):
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

# get attractions with 2 query : page and keyword 
@app.route("/api/attractions")
def get_attractions():
    try:
        page = int(request.args.get('page'))
        keyword = request.args.get('keyword')
        
        # query without keyword
        if not keyword:
            # database query 
            cursor.execute('SELECT * FROM attractions')
            results = cursor.fetchall()
            
            # calculate total page and assign nextPage value
            page_count = cursor.rowcount // 12
            if page < page_count:
                next_page = page + 1
            else:
                next_page = None
            
            # create the whole scenes list
            scene_list = []
            for result in results:
                scene = create_scene_data(result)
                scene_list.append(scene)
            
            # parameters to specify start and end point for each data output page 
            start = page * 12
            end = (page + 1) * 12 
            
            # put processed data into response
            response = {
				"nextPage": next_page,
				"data": scene_list[start:end]
			}
        
        # query without keyword
        else:
            # database query 
            keyword_query = f'SELECT * FROM attractions WHERE name LIKE "%{keyword}%" OR category LIKE "%{keyword}%" OR description LIKE "%{keyword}%" OR address LIKE "%{keyword}%" OR mrt LIKE "%{keyword}%"'
            cursor.execute(keyword_query)
            results = cursor.fetchall()
            
            # calculate total page and assign nextPage value
            page_count = cursor.rowcount // 12
            if page < page_count:
                next_page = page + 1
            else:
                next_page = None
            
            # create the whole scenes list
            scene_list = []
            for result in results:
                scene = create_scene_data(result)
                scene_list.append(scene)

            # parameters to specify start and end point for each data output page 
            start = page * 12
            end = (page + 1) * 12 
            
            # put processed data into response
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
        # query without keyword
        id_query = f'SELECT * FROM attractions WHERE id={attractionId}'
        cursor.execute(id_query)
        result = cursor.fetchone()
        
        # incorrect attraction id
        if not result:
            return make_response(jsonify({"error":True,"message":"景點編號不正確"}),400)
        
        # get scene data and create response
        scene = create_scene_data(result)
        response = {
            "data": scene
        }
        
        return make_response(jsonify(response), 200)
    
    except:
        return make_response(jsonify({"error":True,"message": "伺服器內部出現錯誤"}),500)

if __name__ == '__main__':
    app.run(port=3000,host="0.0.0.0")
