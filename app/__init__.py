from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ
import os

load_dotenv('.flaskenv')

DB_NAME = environ.get('SQLITE_DB')
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'gametrack'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

db = SQLAlchemy(app)


from app import routes, models

def init_db():
    from .models import User
    
    admin_accounts = [
        {'username': 'hec', 'email': 'hec@example.com', 'password': 'lazu'},
        {'username': 'work', 'email': 'work@example.com', 'password': 'please'},
        {'username': 'merin', 'email': 'merin@gmail.com', 'password': 'working'},
        {'username': 'kaye', 'email': 'kaye@gmail.com', 'password': 'still' }
        ]
                
    for info in admin_accounts:
        existing_admin = User.query.filter_by(username=info['username']).first()
        if existing_admin is None:
            new_admin = User(username=info['username'], password=info['password'], email=info['email'])
            new_admin.admin = True
            db.session.add(new_admin)
                    
    db.session.commit()

    


