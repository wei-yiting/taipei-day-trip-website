from flask import Blueprint, json, request, make_response, jsonify, session
import requests
from datetime import datetime
import time
from model.order import db_new_order, db_update_order_status, db_get_order
from model.booking import db_delete_booking

order_api = Blueprint('order_api', __name__, url_prefix='/api')


@order_api.route('/orders', methods=['POST'])
def pay_order():
    try:
        if 'id' not in session:
            return  make_response(jsonify({
                "error": True,
                "message": "f: Please log in"
                }),403)
        
        request_data = request.get_json()
        
        if not (request_data.get('prime') and request_data.get('order')):
            return  make_response(jsonify({
                "error": True,
                "message": "g: incorrect request format"
                }),400)
            
        user_id = session['id']
        order_time = str(datetime.now())
        order_json = json.dumps(request_data.get('order'))
        contact_json = json.dumps(request_data.get('contact'))
        status = 1 # not pay
        
        # produce order number using timestamp
        now_time_str = str(order_time)
        struct_time = time.strptime(now_time_str, "%Y-%m-%d %H:%M:%S.%f")
        time_stamp = int(time.mktime(struct_time))
        order_num = str(time_stamp)
        
        db_new_order(time=order_time, 
                     order_num=order_num, 
                     order_json=order_json, 
                     contact_json=contact_json, 
                     status= status, 
                     user_id=user_id)
        
        # build data for TapPay request
        prime = request_data.get('prime')
        price = request_data.get('order').get('price')

        contact_name = request_data.get('contact').get('name')
        contact_phone = request_data.get('contact').get('phone')
        contact_email = request_data.get('contact').get('email')
        
        tappay_request_headers = {
            "Content-Type": "application/json", 
            "x-api-key": "partner_kjS2J0MSeEiA4UDkY8BO59BUIcnIyID3BP4SBraRP7QupGym29IvUT0D"
            }
        tappay_request_body = {
            "prime": prime,
            "partner_key": "partner_kjS2J0MSeEiA4UDkY8BO59BUIcnIyID3BP4SBraRP7QupGym29IvUT0D",
            "merchant_id": "WYT_CTBC",
            "details":"TapPay Test",
            "amount": price,
            "cardholder": {
                "name": contact_name,
                "phone_number": contact_phone,
                "email": contact_email,
            },
        "remember": True
        }
        
        tappay_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
        
        req = requests.post(tappay_url, data=json.dumps(tappay_request_body), headers=tappay_request_headers)
        res = req.json()
        status = res.get('status')
        error_msg = res.get('msg')
        trade_id = res.get('rec_trade_id')
        
        if status == 0:
            db_update_order_status(order_num,status, trade_id)
            
            # remove bookings from db
            booking_trips = request_data['order']['trip']
            for trip in booking_trips:
                attr_id = trip['attraction']['id']
                db_delete_booking(user_id,attr_id)
            
            res_body = {
                "data":{
                    "number":order_num,
                    "payment":{
                        "status": 0,
                        "message": "付款成功"
                    }
                }
            }
                    
        else:
            res_body = {
                "data":{
                    "number":order_num,
                    "payment":{
                        "status": 1,
                        "message": "付款失敗",
                        "error_detail": error_msg
                    }
                }
            }
        
        return make_response(jsonify(res_body),200)

            
    except Exception as e:
        return make_response(jsonify({
            "error": True,
  			"message": str(e)
            }),500)


@order_api.route('/orders/<order_num>', methods=['GET'])
def get_order(order_num):
    # try:
        if 'id' not in session:
            return  make_response(jsonify({
                "error": True,
                "message": "f: Please log in"
                }),403)
            
        res = db_get_order(order_num)
        return make_response(jsonify(res),200)
        
    # except Exception as e:
    #     return make_response(jsonify({
    #         "error": True,
  	# 		"message": str(e)
    #         }),500)