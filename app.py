import os
from flask import *
from model import app
from api_routes.attraction import attraction_api
from api_routes.user import user_api


############################
######### set up  ##########
############################

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False

app.secret_key = os.urandom(24)



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

# Attractions APIs
app.register_blueprint(attraction_api)
# Users APIs
app.register_blueprint(user_api)




if __name__ == '__main__':
    app.run(port=3000,host="0.0.0.0", debug=True)
