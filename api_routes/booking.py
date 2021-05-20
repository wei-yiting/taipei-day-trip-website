from flask import Blueprint, json, request, make_response, jsonify, session
import datetime
from model.booking import db_get_user_booking, db_store_new_booking, db_check_booking_exist, db_delete_booking

booking_api = Blueprint('booking_api', __name__, url_prefix='/api')


@booking_api.route('/booking', methods=['GET'])
def get_booking_info():
    try:
        if 'id' not in session:
           return  make_response(jsonify({
            "error": True,
  			"message": "f: Please log in"
            }),403)
        else:
            user_id = session['id']
            user_bookings = db_get_user_booking(user_id)
            if not user_bookings:
                return make_response(jsonify({"data": None}),200)
            else:
                booking_list = []
                for booking in user_bookings:
                    booking_attraction = {}
                    booking_attraction['id'] = booking['id']
                    booking_attraction['name'] = booking['name']
                    booking_attraction['address'] = booking['address']
                    booking_attraction['image'] = booking['images'].split(',')[0]
                    booking_info = {}
                    booking_info['attraction'] = booking_attraction
                    booking_info['date'] = booking['date']
                    booking_info['time'] = booking['time']
                    booking_info['price'] = booking['price']
                    booking_list.append(booking_info)
                
                return make_response(jsonify({
                    "data":booking_list
                }),200) 
            
    except Exception as e:
        return make_response(jsonify({
            "error": True,
  			"message": str(e)
            }),500)


@booking_api.route('/booking', methods=['POST'])
def create_new_booking():
    try:
        if 'id' not in session:
           return  make_response(jsonify({
            "error": True,
  			"message": "f: Please log in"
            }),403)
        
        else:
            request_data = request.get_json()
            attr_id = request_data.get('attractionId')
            date_input = request_data.get('date')
            time = request_data.get('time')
            price = request_data.get('price')
            
            date_array = date_input.split('-')
            booking_date = datetime.datetime(int(date_array[0]),int(date_array[1]),int(date_array[2]))
            
            wrong_format_res = make_response(jsonify({
                                "error": True,
                                "message": "g: incorrect request format"
                                }),400)
            
            if attr_id and date_input and time and price:
                
                user_id = session['id']
                if not isinstance(attr_id, int) or attr_id < 1 or attr_id > 319:
                    return wrong_format_res
                if booking_date <= datetime.datetime.now():
                    return wrong_format_res
                if time != 'morning' and time !='afternoon':
                    return wrong_format_res
                
                if db_check_booking_exist(user_id,attr_id):
                    return make_response(jsonify({
                                "error": True,
                                "message": "h: this booking already exists"
                                }),400)
                
                if db_store_new_booking(date_input, time, price, user_id, attr_id):
                    return make_response(jsonify({"ok":True})) 
                
            else:
                return wrong_format_res 
            
            
    except Exception as e:
        return make_response(jsonify({
            "error": True,
  			"message": str(e)
            }),500)


@booking_api.route('/booking', methods=['DELETE'])
def delete_booking():
    try:
        if 'id' not in session:
               return  make_response(jsonify({
            "error": True,
  			"message": "f: Please log in"
            }),403)
        
        user_id = session['id']
        request_data = request.get_json()
        attr_id = request_data.get('attractionId')
        if not attr_id:
            return make_response(jsonify({
                                "error": True,
                                "message": "g: incorrect request format"
                                }),400)
        else:
            if not db_check_booking_exist(user_id,attr_id):
                return make_response(jsonify({
                                    "error": True,
                                    "message": "h: unable to delete, this is not an existed booking"
                                    }),400)
            else:
                if db_delete_booking(user_id,attr_id):
                    return make_response(jsonify({"ok":True})) 
            
    except Exception as e:
        return make_response(jsonify({
            "error": True,
  			"message": str(e)
            }),500)