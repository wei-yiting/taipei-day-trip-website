from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DbCfg



app = Flask('__main__')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DbCfg.usr}:{DbCfg.pwd}@{DbCfg.host}/{DbCfg.db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


