from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField, DateField, RadioField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, StopValidation
from wtforms.widgets import CheckboxInput, ListWidget

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = StringField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')
