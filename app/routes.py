
from flask import Flask, render_template, redirect, url_for, flash, session
from app.forms import LoginForm, RegisterForm, ChangePasswordForm
from app.models import User, Game, Task, Planner
from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sys

#this function stores the user_id in the session after every route, allowing us to identify each user
def load_user(user_id):
    return User.query.get(int(user_id))

#temporary home page
@app.route('/home')
def homepage():
	return "Temporary Home page"

#temporary logged in page to test if/when users have successfully logged in
@app.route('/loggedin')
def loggedin():
     return "Temporary logged in page"

@app.route('/register', methods=['GET', 'POST'])
def registration(): 
      form = RegisterForm()
      #validate_on_submit checks if the request is a post or not
      if form.validate_on_submit():
            #takes the inputted password and transformed it into a hash, to better secure the accounts
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            #after inputting all the new information, it is added and committed into the db
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
      


@app.route('/login', methods=['GET', 'POST'])
def signin():
      form = LoginForm()
      #validate_on_submit checks if the request is a post or not
      if form.validate_on_submit():
        #filters throug the db by username and then checks if the hashed password is the same as the inputted
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            #if successfuk the user is logged in
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('loggedin'))
        else:
			#else the user is denied access
            flash('Invalid username or password', 'danger')

@app.route('/logout')				
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
