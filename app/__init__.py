from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ

load_dotenv('.flaskenv')

DB_NAME = environ.get('SQLITE_DB')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gametrack'

DB_CONFIG_STR = 'sqlite:///' + DB_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

db = SQLAlchemy(app)

from app import routes, models