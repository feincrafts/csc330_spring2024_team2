from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField, IntegerField, DateField, RadioField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, StopValidation
from wtforms.widgets import CheckboxInput, ListWidget

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = StringField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    passwordRepeat = PasswordField('Confirm Password', validators = [DataRequired()])
    submit = SubmitField('Register')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired()])
    submit = SubmitField('Change Password')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators = [DataRequired()])
    new_password_Repeat = PasswordField('Confirm New Password', [DataRequired()])
    submit = SubmitField('Change Password')
    
class CreateEventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired()])
    game = StringField('Game',validators=[DataRequired ()])
    date = DateField('Date', validators = [DataRequired()])
    description =  TextAreaField('Event Description', validators = [DataRequired()])
    participants = IntegerField('Number of Participants', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CreateTaskForm(FlaskForm):
    #title = StringField('Task Title', validators=[DataRequired()])
    game = StringField('Game',validators=[DataRequired ()])
    #date = DateField('Date', validators = [DataRequired()])
    description =  TextAreaField('Add Task', validators = [DataRequired()])
    submit = SubmitField('Submit')

class AddGameForm(FlaskForm):
    game_name = StringField('Show Game tasks', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddNewGameForm(FlaskForm):
    new_game_name = StringField('Add New Game to Database', validators=[DataRequired()])
    submit = SubmitField('Submit')