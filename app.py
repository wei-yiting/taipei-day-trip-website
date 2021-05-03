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
        pool_size = 10,
        host = DbCfg.host,
        user = DbCfg.usr,
        password = DbCfg.pwd,
        database = DbCfg.db
 )


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
num_per_page = 12


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
        sitedb = connectionpool.get_connection()
        cursor = sitedb.cursor()
        
        page = int(request.args.get('page'))
        keyword = request.args.get('keyword')
        
        # query without keyword
        if not keyword:

            # database query 
            start_point = page * num_per_page
            query = f'SELECT * FROM attractions LIMIT {start_point},{num_per_page}'
            cursor.execute(query)
            results = cursor.fetchall()            
            
            #calculate total page and assign nextPage value
            count_query = 'SELECT COUNT(*) FROM attractions'
            cursor.execute(count_query)
            result_count = cursor.fetchone()[0]        
            
            page_count = result_count // num_per_page
            if page < page_count:
                next_page = page + 1
            else:
                next_page = None
            
            # create the whole scenes list
            scene_list = []
            for result in results:
                scene = create_scene_data(result)
                scene_list.append(scene)
                        
            # put processed data into response
            response = {
				"nextPage": next_page,
				"data": scene_list
			}
        
        # query without keyword
        else:
            # database query 
            start_point = page * num_per_page
            keyword_query_condition = f'''
            WHERE name LIKE "%{keyword}%" 
            OR category LIKE "%{keyword}%" 
            OR description LIKE "%{keyword}%" 
            OR address LIKE "%{keyword}%" 
            OR mrt LIKE "%{keyword}%" 
            '''
            keyword_query = f'SELECT * FROM attractions {keyword_query_condition}  LIMIT {start_point},{num_per_page}'
            cursor.execute(keyword_query)
            results = cursor.fetchall()
            
            # calculate total page and assign nextPage value
            count_query = f'SELECT COUNT(*) FROM attractions {keyword_query_condition}'
            cursor.execute(count_query)
            result_count = cursor.fetchone()[0]        
            
            page_count = result_count // num_per_page
            if page < page_count:
                next_page = page + 1
            else:
                next_page = None
            
            # create the whole scenes list
            scene_list = []
            for result in results:
                scene = create_scene_data(result)
                scene_list.append(scene)
            
            # put processed data into response
            response = {
				"nextPage": next_page,
				"data": scene_list
			}
        
        sitedb.close()
        return make_response(jsonify(response),200)
    
    except Exception as e:
        return make_response(jsonify({
			"error": True,
  			"message": str(e)
		}),500)
             

##### get single attraction by id #####
@app.route('/api/attraction/<attractionId>')
def get_attraction(attractionId):
    try:
        sitedb = connectionpool.get_connection()
        cursor = sitedb.cursor()
        
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
        
        sitedb.close()
        return make_response(jsonify(response), 200)
    
    except Exception as e:
        return make_response(jsonify({
			"error": True,
  			"message": str(e)
		}),500)

if __name__ == '__main__':
    app.run(port=3000,host="0.0.0.0")
