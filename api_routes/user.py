from model.user import account_exist, add_new_user, password_check, get_user_info
from flask import Blueprint, request, make_response, jsonify, session

user_api = Blueprint('user_api', __name__, url_prefix='/api')


@user_api.route('/user', methods=['GET'])
def get_user():
    if 'id' in session:
       id = session['id']
       user_info = get_user_info(id)
    else:
        user_info = None
        
    return make_response(jsonify({
        "data":user_info
    }),200)    
    

@user_api.route('/user', methods=['POST'])
def sign_up():
    try:
        # user already logged in
        if 'id' in session:
            return make_response(jsonify({
            "error": True,
  			"message": "a: Please log out first"
            }),400)
            
        request_data = request.get_json()
        
        name = request_data['name']
        email = request_data['email']
        password = request_data['password']
        
        if name and email and password: # check if all credential is given
            is_duplicated = account_exist(email) 
            if is_duplicated: # check if email already registered
                return make_response(jsonify({
                    "error": True,
                    "message": "b:This email is already registered"
                }),400)
            else:
                add_new_user(name, email, password)
                return make_response(jsonify({
                    "ok": True
                }),200)
        
        else:
            return make_response(jsonify({
            "error": True,
  			"message": "c:Missing credentials"
            }),400)
        
    except Exception as e:
        return make_response(jsonify({
            "error": True,
  			"message": str(e)
        }),500)
          
    

@user_api.route('/user', methods=['PATCH'])
def log_in():
    try:
        if 'id' in session:
            return make_response(jsonify({
        "error": True,
        "message": "a: Please log out first"
        }),400) 
        
        request_data = request.get_json()
                
        email = request_data['email']
        password = request_data['password']
        
        if email and password: # check if all credential is given
            
            is_valid_account = account_exist(email)
            if is_valid_account: # check if email accont exist
                
                password_match_id = password_check(email,password)
                if password_match_id: # check if password is correct
                    session['id'] = password_match_id
                    return make_response(jsonify({
                    "ok": True
                    }),200)
                    
                else:
                    return make_response(jsonify({
                    "error": True,
                    "message": "d:Incorrect Password"
                }),400)
                
            else:
                return make_response(jsonify({
                    "error": True,
                    "message": "e:This email has not been registered yet"
                }),400)
                
        else:
            return make_response(jsonify({
            "error": True,
  			"message": "c:Missing credentials"
            }),400)
            
    except Exception as e:
        return make_response(jsonify({
            "error": True,
  			"message": str(e)
            }),500)
   

@user_api.route('/user', methods=['DELETE'])
def log_out():
   session.pop('id', None)
   return make_response(jsonify({
       "ok": True
       }),200)
   
