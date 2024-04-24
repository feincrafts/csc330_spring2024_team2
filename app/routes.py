
from flask import Flask, render_template, redirect, url_for, flash, session
from app.forms import LoginForm, RegisterForm, ResetPasswordForm, ForgotPasswordForm, CreateEventForm, CreateTaskForm
from app.models import *
from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import FlaskLoginClient, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sys
from app import *

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    return get_user(username)
    

"""
#this function stores the user_id in the session after every route, allowing us to identify each user
def load_user(user_id):
    return User.query.get(int(user_id))
"""

@app.route('/')
def default():
    return redirect('/login')

#temporary home page
@app.route('/home', methods=['GET', 'POST'])
#@login_required
def homepage():
	return render_template('planner.html')

#temporary logged in page to test if/when users have successfully logged in
@app.route('/loggedin')
def loggedin():
     return "Temporary successful login page"

@app.route('/loggedin_ad')
def loggedin_ad():
     return 'Temporary login as an admin'

@app.route('/register', methods=['GET', 'POST'])
def registration(): 
    form = RegisterForm()
     #validate_on_submit checks if the request is a post or not
    if form.validate_on_submit():
        if form.password.data != form.passwordRepeat.data: #makes sure passwords match
            return redirect('/register')
         #takes the inputted password and transformed it into a hash, to better secure the accounts
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #after inputting all the new information, it is added and committed into the db
        db.session.add(new_user)
        db.session.commit()
        print("New user registered:", new_user.username)
        print("Hashed Password:", new_user.password)
        return redirect('/login')
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def signin():
    logout_user()
    form = LoginForm()
    #validate_on_submit checks if the request is a post or not
    if form.validate_on_submit():
        #filters throug the db by username and then checks if the hashed password is the same as the inputted
        username_in = form.username.data
        password_in = form.password.data
        user = User.query.filter_by(username=username_in).first()
        print("Username and email: ",user) #prints user and email for now
        if user is None:
            print("User not found")
            return redirect('/register')
        elif user.admin:
            return redirect('/loggedin_ad')
        elif not check_password_hash(user.password, password_in):
             print("PW is wrong")
             return redirect('/login')
        else:
            print("Congrats you logged in")
            login_user(user)
            return redirect('/home')

    return render_template('login.html', form=form)
      
@app.route('/logout')				
def logout():
    try:
        logout_user()
        print("You're logged out!")
    except:
         print("oops logout broke")
    flash('You have been logged out.', 'info')
    return redirect('/login')

@app.route('/forgotpw')
def forgot():
     form = ForgotPasswordForm()
     return render_template('forgotpw.html', form=form)

@app.route('/resetpw')
def reset():
     form = ResetPasswordForm()
     return render_template('resetpw.html', form=form)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
     form = CreateEventForm()

     print()
     if form.validate_on_submit():
        # todo, implement unique id
        # todo implement date
        # todo get way of getting current user
        new_event = Event(title=form.title.data, game=str(form.game.data), date=form.date.data, description=form.description.data, participants=form.participants.data)
        #after inputting all the new information, it is added and committed into the db
        db.session.add(new_event)
        print(new_event)
        db.session.commit()
        return redirect('/calendar')
     return render_template('create_event.html', form=form)

@app.route('/calendar', methods=['GET','POST'])
def calendar():
     # to get more info, elaborate on this and adjust models.py repr
     # todo filter by current user 
     # todo - how to store/get current user??? 
     results = db.session.query(Event.title, Event.date, Event.description)
     #results = Event.query.filter_by(user=task.user) #ignore this it doesn't work
     return render_template('calendar.html', events=results)

@app.route('/settings')
def settings():
     return render_template('settings.html')

     return render_template('create_event.html', form=form)

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
     form = CreateTaskForm()
     return render_template('create_task.html', form=form)