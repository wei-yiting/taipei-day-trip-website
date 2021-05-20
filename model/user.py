from model import db
from model.models import User
import datetime


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