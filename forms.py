from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, Email
from states import US_STATES

STATES = US_STATES.keys()


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
    state_id = SelectField('State', choices=[(state, state) for state in STATES], validators=[
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
    state_id = SelectField('State', choices=[(state, state) for state in STATES], validators=[
        InputRequired(message='This field is required')])
    zip_code = StringField('Zip Code', validators=[InputRequired(message='This field is required'), Length(
        min=5, max=20, message='Please enter a valid length between 5 and 20 characters')])


class UserLoginForm(FlaskForm):
    """Form for user"""
    username = StringField('Username', validators=[InputRequired(message='Please enter a Username'), Length(
        min=1, max=50, message='Please select a valid length of between 1 and 50 characters')])
    password = PasswordField('Password', validators=[
        InputRequired(message='Please enter a password')])


class SendPasswordResetForm(FlaskForm):
    """Form for sending password reset link"""
    email = StringField('Email Address', validators=[InputRequired(
        message='This field is required'), Email(message='Please enter a valid email address')])


class ResetPasswordForm(FlaskForm):
    """Form for resetting password"""
    password = PasswordField('Password', validators=[
        InputRequired(message='Please enter a password')])


class StateEditForm(FlaskForm):
    """Form for editing state info as Admininistrator"""
    registration_url = StringField('Registration URL')
    elections_url = StringField('Elections URL')
    registration_in_person_deadline = StringField(
        'Voter Registration Deadline: In-Person')
    registration_mail_deadline = StringField(
        'Voter Registration Deadline: Mail')
    registration_online_deadline = StringField(
        'Voter Registration Deadline: Online')
    absentee_application_in_person_deadline = StringField(
        'Absentee Ballot Application Deadline: In-Person')
    absentee_application_mail_deadline = StringField(
        'Absentee Ballot Application Deadline: Mail')
    absentee_application_online_deadline = StringField(
        'Absentee Ballot Application Deadline: Online')
    voted_absentee_ballot_deadline = StringField(
        'Voted Absentee Ballot Due Date')
    check_registration_url = StringField(
        'URL to Check Voter Registration Status')
    polling_location_url = StringField('URL to Check Polling Location')
    absentee_ballot_url = StringField('Absentee Ballot URL')
    local_election_url = StringField(
        'Local Election Office/Clerk Information URL')
    ballot_tracker_url = StringField('Absentee/Mail Ballot Tracker URL')

class StateRegistrationRuleForm(FlaskForm):
    """Form for adding new registration rules as Administrator"""
    rule = StringField('Registration Rule', validators=[InputRequired(message='Input Required')])
    
class ElectionForm(FlaskForm):
    """Form for adding new elections as Administrator"""
    name = StringField('Election Name', validators=[InputRequired(message='Input Required')])
    date = DateField ('Date of Election', validators=[InputRequired(message='Input Required')])
    state_id = SelectField('State of Election', choices=[(state, state) for state in STATES], validators=[
        InputRequired(message='This field is required')])
    
class AdminUserForm(FlaskForm):
    """Admin Form for Editing user"""
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
    state_id = SelectField('State', choices=[(state, state) for state in STATES], validators=[
        InputRequired(message='This field is required')])
    zip_code = StringField('Zip Code', validators=[InputRequired(message='This field is required'), Length(
        min=5, max=5, message='Please enter zip code length of 5 characters'), ])
    is_admin = BooleanField('Administrator', validators=[InputRequired(message='This field is required')])