from app import db

class Users(Use, db.Model): 
	Userid = db.Column(db.Integer, primary_key=True)
	
	username = db.Column(db.String(250), unique=True,nullable=False)
    	password = db.Column(db.String(250), nullable=False)
