from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, Email


STATES = [
    'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA',
    'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA',
    'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND',
    'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
    'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY'
]


class NewUserForm(FlaskForm):
    """Form for user"""
    username = StringField('Username', validators=[InputRequired(message='Please enter a Username'), Length(
        min=4, max=50, message='Please select a valid length of between 4 and 50 characters')])
    password = PasswordField('Password', validators=[
                             InputRequired(message='Please enter a password of at least 8 characters'), Length(
                                 min=8, max=255, message='Please select a valid length of between 8 and 255 characters')])
    email = StringField('Email Address', validators=[InputRequired(message='This field is required'), Length(
        min=6, max=255, message='Please enter a valid length between 6 and 255 characters'), Email(message='Please enter a valid email address')])
    first_name = StringField('First Name', validators=[InputRequired(message='This field is required'), Length(
        min=1, max=255, message='Please enter a valid length between 1 and 255 characters')])
    last_name = StringField('Last Name', validators=[InputRequired(message='This field is required'), Length(
        min=1, max=255, message='Please enter a valid length between 1 and 255 characters')])
    street_address = StringField('Street Address', validators=[
                                 InputRequired(message='This field is required')])
    city = StringField('City', validators=[InputRequired(message='This field is required'), Length(
        min=1, max=255, message='Please enter a valid length between 1 and 255 characters')])
    state = SelectField('State', choices=[(state, state) for state in STATES], validators=[
                        InputRequired(message='This field is required')])
    zip_code = StringField('Zip Code', validators=[InputRequired(message='This field is required'), Length(
        min=5, max=5, message='Please enter zip code length of 5 characters'), ])


class EditUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(message='This field is required'), Length(
        min=1, max=255, message='Please enter a valid length between 1 and 255 characters')])
    last_name = StringField('Last Name', validators=[InputRequired(message='This field is required'), Length(
        min=1, max=255, message='Please enter a valid length between 1 and 255 characters')])
    street_address = StringField('Street Address', validators=[
                                 InputRequired(message='This field is required')])
    city = StringField('City', validators=[InputRequired(message='This field is required'), Length(
        min=1, max=255, message='Please enter a valid length between 1 and 255 characters')])
    state = SelectField('State', choices=[(state, state) for state in STATES], validators=[
                        InputRequired(message='This field is required')])
    zip_code = StringField('Zip Code', validators=[InputRequired(message='This field is required'), Length(
        min=5, max=20, message='Please enter a valid length between 5 and 20 characters')])


class UserLoginForm(FlaskForm):
    """Form for user"""
    username = StringField('Username', validators=[InputRequired(message='Please enter a Username'), Length(
        min=1, max=50, message='Please select a valid length of between 1 and 50 characters')])
    password = PasswordField('Password', validators=[
        InputRequired(message='Please enter a password')])
