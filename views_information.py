from app import app
from flask import Flask, render_template, request, redirect, session, flash, jsonify, abort, send_from_directory, url_for, json
from flask_mail import Mail, Message
import json
import easypost
import requests
import geocoder

from forms import NewUserForm, UserLoginForm, EditUserForm, SendPasswordResetForm, ResetPasswordForm, StateEditForm, StateRegistrationRuleForm, ElectionForm, AdminUserForm
from models import connect_db, db, User, State, Election, RegistrationRule

from sqlalchemy.exc import IntegrityError
import os
import lob

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod == None:
    from api_keys import LOB_API_KEY, GOOGLE_CIVIC_API_KEY, MAPQUEST_API_KEY, EASYPOST_API_KEY
    from secret_keys import MAIL_USERNAME, MAIL_PASSWORD, SECRET_KEY
if is_prod:
    LOB_API_KEY = os.environ.get('LOB_API_KEY')
    EASYPOST_API_KEY = os.environ.get('EASYPOST_API_KEY')
    GOOGLE_CIVIC_API_KEY = os.environ.get('GOOGLE_CIVIC_API_KEY')
    MAPQUEST_API_KEY = os.environ.get('MAPQUEST_API_KEY')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY')

# Views for Information Routes

@app.route('/elections')
def get_elections():
    """Returns local elections"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.filter(
        User.username == session.get('username')).first()
    address = f'{curr_user.street_address} {curr_user.city} {curr_user.state_id} {curr_user.zip_code}'
    resp = requests.get(
        f'https://www.googleapis.com/civicinfo/v2/voterinfo?key={GOOGLE_CIVIC_API_KEY}&address={address}').text
    response_info = json.loads(resp)
    elections = Election.query.filter(
        Election.state_id == curr_user.state_id).order_by(Election.date).all()
    return render_template('elections.html', user=curr_user, data=response_info, elections=elections)


@app.route('/state-information')
def get_state_info():
    """Returns info on user's state to user including election links and voter registration links"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.filter(
        User.username == session.get('username')).first()
    address = f'{curr_user.street_address} {curr_user.city} {curr_user.state_id} {curr_user.zip_code}'
    resp = requests.get(
        f'https://www.googleapis.com/civicinfo/v2/representatives?key={GOOGLE_CIVIC_API_KEY}&address={address}').text
    response_info = json.loads(resp)
    return render_template('state-info.html', user=curr_user, data=response_info)

@app.route('/officials')
def get_officials():
    """Returns local representatives from user's address"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.filter(
        User.username == session.get('username')).first()
    address = f'{curr_user.street_address} {curr_user.city} {curr_user.state_id} {curr_user.zip_code}'
    resp = requests.get(
        f'https://www.googleapis.com/civicinfo/v2/representatives?key={GOOGLE_CIVIC_API_KEY}&address={address}').text
    response_info = json.loads(resp)
    return render_template('officials.html', resp=response_info, user=curr_user)