from model import db

##### create attraction model #####
class Attraction(db.Model):
    
    __tablename__ = 'attractions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    transport = db.Column(db.Text)
    mrt = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    images = db.Column(db.Text)
    
    db_attraction_booking = db.relationship("Booking", backref="attractions", lazy='dynamic')
    db_attraction_collection = db.relationship("Collection", backref="attractions", lazy='dynamic')
    
    
    def __init__(self, name, category, description, address, transport, mrt, latitude, longitude, images):
        self.name = name
        self.category = category
        self.description = description
        self.address = address
        self.transport = transport
        self.mrt = mrt
        self.latitude = latitude
        self.longitude = longitude
        self.images = images


##### create user model #####

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255,collation='binary'), nullable=False)
    password = db.Column(db.String(255,collation='binary'), nullable=False)
    time = db.Column(db.DateTime)
    
    db_user_booking = db.relationship("Booking", backref="users",lazy='dynamic')
    db_user_collection = db.relationship("Collection", backref="users", lazy='dynamic')
    
    def __init__(self,name,email,password,time):
        self.name = name
        self.email = email
        self.password = password
        self.time = time


##### create booking model #####

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'), nullable=False)
    
    def __init__(self, date, time, price, user_id, attraction_id):
        self.date = date
        self.time = time
        self.price = price
        self.user_id = user_id
        self.attraction_id = attraction_id


##### create model #####
class Collection(db.Model):
    __tablename__ = 'collections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'), nullable=False)
    
    def __init__(self, user_id, attraction_id):
        self.user_id = user_id
        self.attraction_id = attraction_id



db.create_all()