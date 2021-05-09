from flask import Blueprint, request, make_response, jsonify
from model.attraction import get_attractions_data, get_attractions_count, get_attraction_by_id
from utils.create_attraction import create_attraction_data
attraction_api = Blueprint('attraction_api', __name__, url_prefix='/api')


##### get attractions page #####
num_per_page = 12

@attraction_api.route("/attractions")
def get_attractions():
    try:
        page = int(request.args.get('page'))
        keyword = request.args.get('keyword')
        start_point = page * num_per_page
        
        # database query 
        results = get_attractions_data(num_per_page, start_point, keyword)
        result_count = get_attractions_count(keyword)

        #calculate total page and assign nextPage value
        page_count = result_count // num_per_page
        if page < page_count:
            next_page = page + 1
        else:
            next_page = None
        
        # create the whole scenes list
        scene_list = []
        for result in results:
            scene = create_attraction_data(result)
            scene_list.append(scene)
                    
        # put processed data into response
        response = {
            "nextPage": next_page,
            "data": scene_list
        }
    
        return make_response(jsonify(response),200)
    
    except Exception as e:
        return make_response(jsonify({
			"error": True,
  			"message": str(e)
		}),500)
             

##### get single attraction by id #####
@attraction_api.route('/attraction/<attractionId>')
def get_attraction(attractionId):
    try:
        
        # query attraction
        result = get_attraction_by_id(attractionId)
        
        # incorrect attraction id
        if not result:
            return make_response(jsonify({"error":True,"message":"景點編號不正確"}),400)
        
        # get scene data and create response
        scene = create_attraction_data(result)
        response = {
            "data": scene
        }
        
        return make_response(jsonify(response), 200)
    
    except Exception as e:
        return make_response(jsonify({
			"error": True,
  			"message": str(e)
		}),500)