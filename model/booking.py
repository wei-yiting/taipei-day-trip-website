from model import db
from model.models import Booking
from model.models import Attraction

def db_get_user_booking(user_id):
    query = f'''
    SELECT bookings.date, bookings.time, bookings.price, 
    attractions.id, attractions.name, attractions.address, attractions.images 
    FROM bookings
    JOIN attractions on bookings.attraction_id = attractions.id 
    WHERE bookings.user_id = {user_id}
    '''
    results = db.engine.execute(query).fetchall()
    return results
    
        


def db_check_booking_exist(user_id,attr_id):
    all_user_bookings = Booking.query.filter_by(user_id=user_id).all()
    for user_booking in all_user_bookings:
        if user_booking.attraction_id == attr_id:
            return True
    return False


def db_store_new_booking(date,time,price,user_id,attr_id):
    new_booking = Booking(date,time,price,user_id,attr_id)
    db.session.add(new_booking)
    db.session.commit()
    return True


def db_delete_booking(user_id, attr_id):
    booking_to_delete = Booking.query.filter_by(user_id=user_id,attraction_id=attr_id).first()
    db.session.delete(booking_to_delete)
    db.session.commit()
    return True
