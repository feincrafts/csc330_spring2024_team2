
from flask import Flask, render_template, redirect, url_for, flash, session
from app.forms import LoginForm, RegisterForm, ResetPasswordForm, ForgotPasswordForm
from app.models import User, Game, Task, Planner
from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sys
from app import *

#this function stores the user_id in the session after every route, allowing us to identify each user
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def default():
    return redirect('/login')

#temporary home page
@app.route('/home')
def homepage():
	return render_template('planner.html')

#temporary logged in page to test if/when users have successfully logged in
@app.route('/loggedin')
def loggedin():
     return "Temporary successful login page"

@app.route('/register', methods=['GET', 'POST'])
def registration(): 
      form = RegisterForm()
      #validate_on_submit checks if the request is a post or not
      if form.validate_on_submit():
            #takes the inputted password and transformed it into a hash, to better secure the accounts
            password = form.password.data
            new_user = User(username=form.username.data, email=form.email.data, password=password)
            #after inputting all the new information, it is added and committed into the db
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect('/login')
      return render_template('signup.html', form=form)
      


@app.route('/login', methods=['GET', 'POST'])
def signin():
      form = LoginForm()
      #validate_on_submit checks if the request is a post or not
      if form.validate_on_submit():
        #filters throug the db by username and then checks if the hashed password is the same as the inputted
        username = form.username.data
        user = db.session.query(User).filter_by(username=username).first()
        if user is None:
            form.password.data = ''
            form.username.data = ''
            return render_template('signup.html', form=form)
        if not user.check_password is None:
            form.password.data = ''
            form.username.data = ''
            return render_template('signup.html', form=form)
            #if successfuk the user is logged in
        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect('/loggedin')
      return render_template('planner.html', form=form)
      
@app.route('/logout')				
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/forgotpw')
def forgot():
     form = ForgotPasswordForm()
     return render_template('forgotpw.html', form=form)

@app.route('/resetpw')
def reset():
     form = ResetPasswordForm()
     return render_template('resetpw.html', form=form)
