from flask import Flask, render_template, request, redirect, session, flash, jsonify, abort, send_from_directory, url_for, json
import json
from api_keys import LOB_API_KEY, GOOGLE_CIVIC_API_KEY, OPEN_FEC_API_KEY, ELECTIONS_ONLINE_API_KEY
import requests
from state_info import STATE_REGISTRATION_URLS, US_STATES, STATE_ELECTION_INFO_URLS

from forms import NewUserForm, UserLoginForm, EditUserForm
from models import connect_db, db, User

from sqlalchemy.exc import IntegrityError
import os
import lob
lob.api_key = LOB_API_KEY

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')

URI = os.environ.get('DATABASE_URL', 'postgresql:///voter-db')
if URI.startswith("postgres://"):
    URI = URI.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get(
    'SECRET_KEY', 'M8)\x92\xb6Gk\xeeR\xc7jr')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
connect_db(app)


@app.route('/')
def index():
    """Landing Page"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration Page"""
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = User.register(username, form.password.data).password
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        street_address = form.street_address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        new_user = User(username=username, password=password,
                        email=email, first_name=first_name, last_name=last_name, street_address=street_address, city=city, state=state, zip_code=zip_code)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors = [
                'Sorry - this username or email is already registered']
            form.email.errors = [
                'Sorry - this username or email address is already registered']
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash(f'Welcome {new_user.username}!', 'success')
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)


@app.route('/verify-address', methods=['POST'])
def verify_user_address():
    """Verifies user address through Lob API"""
    form = NewUserForm()
    verify_response = {'response': {}, 'errors': {}}
    street_address = request.json['street_address']
    city = request.json['city']
    state = request.json['state']
    zip_code = request.json['zip_code']
    resp = lob.USVerification.create(
        address=f'{street_address} {city} {state} {zip_code}')
    if resp['deliverability'] == 'undeliverable':
        verify_response['errors']['error'] = 'Invalid address'
        print('INVALID ADDRESS!')
        return jsonify(verify_response)
    verified_first_line = resp['primary_line']
    if resp['secondary_line']:
        verified_second_line = resp['secondary_line']
        verify_response['response'][
            'verified_street_address'] = f'{verified_first_line} {verified_second_line}'
    else:
        verify_response['response']['verified_street_address'] = verified_first_line
    verify_response['response']['verified_city'] = resp['components']['city']
    verify_response['response']['verified_state'] = resp['components']['state']
    verify_response['response']['verified_zip_code'] = resp['components']['zip_code']
    return jsonify(verify_response)


@app.route('/verify-random-address', methods=['POST'])
def verify_random_address():
    verify_response = {'response': {}, 'errors': {}}
    address = request.json['full_address']
    resp = lob.USVerification.create(
        address=address)
    if resp['deliverability'] == 'undeliverable':
        verify_response['errors']['error'] = 'Invalid address'
        print('INVALID ADDRESS!')
        return jsonify(verify_response)
    verified_first_line = resp['primary_line']
    if resp['secondary_line']:
        verified_second_line = resp['secondary_line']
        verify_response['response'][
            'verified_street_address'] = f'{verified_first_line} {verified_second_line}'
    else:
        verify_response['response']['verified_street_address'] = verified_first_line
    verify_response['response']['verified_city'] = resp['components']['city']
    verify_response['response']['verified_state'] = resp['components']['state']
    verify_response['response']['verified_zip_code'] = resp['components']['zip_code']
    return jsonify(verify_response)


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    """Logs user into site"""
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome back, {user.username}!', 'success')
            session['username'] = user.username
            return redirect(f'/')
        else:
            form.username.errors = ['Invalid Username/Password']
    return render_template('login.html', form=form)


@app.route('/logout')
def log_out_user():
    """Logs user out of site"""
    session.pop('username')
    flash('User logged out!', 'success')
    return redirect('/')


@app.route('/users/<username>')
def show_user_profile(username):
    """Shows profile of current user"""
    print(session['username'])
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    if session['username'] != username:
        flash('Cannot access this page', 'danger')
        return redirect('/')
    user = User.query.get_or_404(username)
    return render_template('user_details.html', user=user)


@app.route('/users/<username>/edit', methods=['GET', 'POST'])
def edit_user_info(username):
    """Edits registered user information for that user"""
    print(session['username'])
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    if session['username'] != username:
        flash('Cannot access this page', 'danger')
        return redirect('/')
    user = User.query.get_or_404(username)
    form = EditUserForm()
    if request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.street_address.data = user.street_address
        form.city.data = user.city
        form.state.data = user.state
        form.zip_code.data = user.zip_code
    if request.method == 'POST':
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.street_address = form.street_address.data
            user.city = form.city.data
            user.state = form.state.data
            user.zip_code = form.zip_code.data
            db.session.commit()
            return redirect(f'/users/{username}')
    return render_template('edit_user.html', form=form, user=user)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Deletes user from database and site"""
    curr_user = User.query.filter(
        User.username == session.get('username')).first()
    user = User.query.filter(User.username == username).first()
    if session.get('username') != username:
        flash('Must be logged in as user to delete', 'danger')
        return redirect('/')
    else:
        deleted_user = User.query.filter(User.username == username).first()
        db.session.delete(deleted_user)
        db.session.commit()
        session.pop('username')
        flash('User deleted', 'success')
        return redirect('/')


@app.route('/representatives')
def get_representatives():
    """Returns local representatives from user's address"""
    curr_user = User.query.filter(
        User.username == session.get('username')).first()
    address = f'{curr_user.street_address} {curr_user.city} {curr_user.state} {curr_user.zip_code}'
    resp = requests.get(
        f'https://www.googleapis.com/civicinfo/v2/representatives?key={GOOGLE_CIVIC_API_KEY}&address={address}').text
    response_info = json.loads(resp)
    divisions = response_info['divisions']
    offices = list(response_info['offices'])
    officials = list(response_info['officials'])
    return render_template('representatives.html', resp=response_info)


@app.route('/elections')
def get_elections():
    """Returns local elections"""
    curr_user = User.query.filter(
        User.username == session.get('username')).first()
    address = f'{curr_user.street_address} {curr_user.city} {curr_user.state} {curr_user.zip_code}'
    resp = requests.get(
        f'https://www.googleapis.com/civicinfo/v2/voterinfo?key={GOOGLE_CIVIC_API_KEY}&address={address}').text
    response_info = json.loads(resp)
    state_elections_url = STATE_ELECTION_INFO_URLS[curr_user.state]
    state_url = STATE_REGISTRATION_URLS[curr_user.state]
    full_state_name = US_STATES[curr_user.state]
    return render_template('elections.html', user=curr_user, full_state_name=full_state_name, data=response_info, state_elections_url=state_elections_url)

@app.route('/registration')
def get_registration_info():
    """Returns info to user on Voter Registration in their State"""
    curr_user = User.query.filter(
        User.username == session.get('username')).first()
    state = curr_user.state
    full_state_name = US_STATES[curr_user.state]
    state_url = STATE_REGISTRATION_URLS[curr_user.state]
    return render_template('registration.html', user=curr_user, state_url=state_url, full_state_name=full_state_name)