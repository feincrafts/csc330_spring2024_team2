from app import app
from flask import render_template, redirect, url_for
from app.forms import LoginForm, RegisterForm, ChangePasswordForm
from app import db
from app.models import 
import sys


@app.route('/register', methods=['POST'])


@app.route('/login', methods=['GET', 'POST'])
def signin():
	username = None
	form = LoginForm()
	
	if form.validate_on_submit():
		
		user =  Users.query.filter_by(
			username=request.form.get('username'))).first()
		if user.password == request.form.get('password'):
			login_user(user)
			return redirect(  //homepage url  )
		else: 
			return 'wrong password or username'
		
	return render_template('login.html')
					
