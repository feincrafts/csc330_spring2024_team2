from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField, DateField, RadioField, BooleanField, SelectField, SelectMultipleField
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

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators = [DataRequired()])
    new_password = PasswordField('New Password', validators = [DataRequired()])
    new_password_Repeat = PasswordField('Confirm New Password', [DataRequired()])
    submit = SubmitField('Change Pasword')
    
class PostForm(FlaskForm):
    post = TextAreaField('Post', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ShopCheckoutForm(FlaskForm):
    points_to_use = StringField('Number of Points', validators = [DataRequired()])
    
