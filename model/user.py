from model import db
import datetime

##### create model #####

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255,collation='binary'), nullable=False)
    password = db.Column(db.String(255,collation='binary'), nullable=False)
    time = db.Column(db.DateTime)
    
    def __init__(self,name,email,password,time):
        self.name = name
        self.email = email
        self.password = password
        self.time = time

db.create_all()


##### functions #####

def account_exist(email):
    if  User.query.filter_by(email=email).first():
        return True
    return False


def add_new_user(name, email, password):
    new_user = User(name=name, email=email, password=password, time=datetime.datetime.now())
    db.session.add(new_user)
    db.session.commit()


def password_check(email,password):
    user = User.query.filter_by(email=email).first()
    if password == user.password.decode('utf-8'):
        return user.id
    return False

def get_user_info(id):
    user = User.query.filter_by(id=id).first()
    user_info = {
        "id": user.id,
        "name": user.name,
        "email": user.email.decode('utf-8')
    }
    return user_info