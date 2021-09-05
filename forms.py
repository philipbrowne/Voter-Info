from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class NewUserForm(FlaskForm):
    """Form for user"""
    username = StringField('Username', validators=[InputRequired(message='Please enter a Username'), Length(
        min=1, max=50, message='Please select a valid length of between 1 and 50 characters')])
    password = PasswordField('Password', validators=[
                             InputRequired(message='Please enter a password')])
    email = StringField('Email Address', validators=[InputRequired(message='Please enter an email address'), Length(
        min=6, max=255, message='Please enter a valid length between 6 and 255 characters'), Email(message='Please enter a valid email address')])


class UserLoginForm(FlaskForm):
    """Form for user"""
    username = StringField('Username', validators=[InputRequired(message='Please enter a Username'), Length(
        min=1, max=50, message='Please select a valid length of between 1 and 50 characters')])
    password = PasswordField('Password', validators=[
                             InputRequired(message='Please enter a password')])
