from model import db
from model.models import Order
import json

def db_new_order(time, order_num, order_json, contact_json, status, user_id):
    new_order = Order(time, order_num, order_json, contact_json, status, None, user_id)
    db.session.add(new_order)
    db.session.commit()
    return True

def db_update_order_status(order_num,status, trade_id):
    current_order = Order.query.filter_by(order_num=order_num).first()
    current_order.status = status
    current_order.trade_id = trade_id
    db.session.add(current_order)
    db.session.commit()
    return True

def db_get_order(order_num):
    order_to_get = Order.query.filter_by(order_num=order_num).first()
    if not order_to_get:
        return {"data": None}
    order_info = json.loads(order_to_get.order_json)
    price = order_info['price']
    trip = order_info['trip']
    contact = json.loads(order_to_get.contact_json)
    status = order_to_get.status
    print(status)
    data = {
        "data":{
            "number": order_num,
            "price": price,
            "trip": trip,
            "contact":contact,
            "status":status
        }
    }
    return data
    