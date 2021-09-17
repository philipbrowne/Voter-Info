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

# Views for User Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration Page"""
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        street_address = form.street_address.data
        city = form.city.data
        state_id = form.state_id.data
        zip_code = form.zip_code.data
        new_user = User(username=username, password=password,
                        email=email, first_name=first_name, last_name=last_name, street_address=street_address, city=city, state_id=state_id, zip_code=zip_code)
        full_address = f'{street_address} {city} {state_id} {zip_code}'
        g = geocoder.mapquest(full_address, key=MAPQUEST_API_KEY)
        if g.geojson['features'][0]['properties'].get('county'):
            county = g.geojson['features'][0]['properties'].get('county')
            new_user.county = county
        try:
            new_user = User.register(username, password, first_name, last_name,
                                     street_address, city, county, state_id, zip_code, email)
            db.session.commit()
        except IntegrityError:
            form.username.errors = [
                'Sorry - this username or email address is already registered']
            form.email.errors = [
                'Sorry - this username or email address is already registered']
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash(f'Welcome {new_user.username}!', 'success')
        return redirect(f'/users/{new_user.username}')
    else:
        if 'username' in session:
            user = User.query.filter(
                User.username == session['username']).first()
            return render_template('register.html', user=user, form=form)
        return render_template('register.html', form=form)


@app.route('/verify-address', methods=['POST'])
def verify_user_address():
    """Verifies user address through EasyPost API"""
    form = NewUserForm()
    verify_response = {'response': {}, 'errors': {}}
    street_address = request.json['street_address']
    city = request.json['city']
    state_id = request.json['state_id']
    zip_code = request.json['zip_code']
    resp = easypost.Address.create(
        verify=['delivery'], street1=street_address, city=city, state=state_id, zip=zip_code)
    success_status = resp['verifications']['delivery']['success']
    if success_status == False:
        verify_response['errors']['error'] = 'Invalid address'
        return jsonify(verify_response)
    if success_status == True:
        verified_first_line = resp['street1']
        if resp['street2']:
            verified_second_line = resp['street2']
            verify_response['response'][
                'verified_street_address'] = f'{verified_first_line} {verified_second_line}'
        else:
            verify_response['response']['verified_street_address'] = verified_first_line
        verify_response['response']['verified_city'] = resp['city']
        verify_response['response']['verified_state'] = resp['state']
        verify_response['response']['verified_zip_code'] = resp['zip'][0:5]
        return jsonify(verify_response)
    # Alternative API available - potential use if EasyPost goes down
    # Verification Using Lob - 300 use Rate Limit
    # resp = lob.USVerification.create(
    #     address=f'{street_address} {city} {state_id} {zip_code}')
    # verified_first_line = resp['primary_line']
    # if resp['secondary_line']:
    #     verified_second_line = resp['secondary_line']
    #     verify_response['response'][
    #         'verified_street_address'] = f'{verified_first_line} {verified_second_line}'
    # else:
    #     verify_response['response']['verified_street_address'] = verified_first_line
    # verify_response['response']['verified_city'] = resp['components']['city']
    # verify_response['response']['verified_state'] = resp['components']['state']
    # verify_response['response']['verified_zip_code'] = resp['components']['zip_code']
    # return jsonify(verify_response)


@app.route('/verify-random-address', methods=['POST'])
def verify_random_address():
    """Verifies Existence of Random Address from AJAX Request"""
    verify_response = {'response': {}, 'errors': {}}
    street1 = request.json['street1']
    city = request.json['city']
    state = request.json['state']
    zip = request.json['zip']
    resp = easypost.Address.create(
        verify=['delivery'], street1=street1, city=city, state=state, zip=zip)
    success_status = resp['verifications']['delivery']['success']
    if success_status == False:
        verify_response['errors']['error'] = 'Invalid address'
        return jsonify(verify_response)
    if success_status == True:
        verified_first_line = resp['street1']
        if resp['street2']:
            verified_second_line = resp['street2']
            verify_response['response'][
                'verified_street_address'] = f'{verified_first_line} {verified_second_line}'
        else:
            verify_response['response']['verified_street_address'] = verified_first_line
        verify_response['response']['verified_city'] = resp['city']
        verify_response['response']['verified_state'] = resp['state']
        verify_response['response']['verified_zip_code'] = resp['zip'][0:5]
        return jsonify(verify_response)
    # Alternative API available - potential use if EasyPost goes down
    # resp = lob.USVerification.create(
    #     address=address)
    # if resp['deliverability'] == 'undeliverable':
    #     verify_response['errors']['error'] = 'Invalid address'
    #     print('INVALID ADDRESS!')
    #     return jsonify(verify_response)
    # verified_first_line = resp['primary_line']
    # if resp['secondary_line']:
    #     verified_second_line = resp['secondary_line']
    #     verify_response['response'][
    #         'verified_street_address'] = f'{verified_first_line} {verified_second_line}'
    # else:
    #     verify_response['response']['verified_street_address'] = verified_first_line
    # verify_response['response']['verified_city'] = resp['components']['city']
    # verify_response['response']['verified_state'] = resp['components']['state']
    # verify_response['response']['verified_zip_code'] = resp['components']['zip_code']
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
    if 'username' in session:
        user = User.query.filter(User.username == session['username']).first()
    return render_template('login.html', form=form)


@app.route('/logout')
def log_out_user():
    """Logs user out of site"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    username = session['username']
    session.pop('username')
    flash(f'{username} has logged out.', 'success')
    return redirect('/')


@app.route('/users/<username>')
def show_user_profile(username):
    """Shows profile of current user"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    if session['username'] != username:
        flash('Cannot access this page', 'danger')
        return redirect('/')
    curr_user = User.query.get_or_404(username)
    address = f'{curr_user.street_address} {curr_user.city} {curr_user.state_id} {curr_user.zip_code}'
    resp = requests.get(
        f'https://www.googleapis.com/civicinfo/v2/representatives?key={GOOGLE_CIVIC_API_KEY}&address={address}').text
    response_info = json.loads(resp)
    return render_template('user_details.html', user=curr_user, data=response_info)


@ app.route('/users/<username>/edit', methods=['GET', 'POST'])
def edit_user_info(username):
    """Edits registered user information for that user"""
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
        form.state_id.data = user.state_id
        form.zip_code.data = user.zip_code
    if request.method == 'POST':
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.street_address = form.street_address.data
            user.city = form.city.data
            user.state_id = form.state_id.data
            user.zip_code = form.zip_code.data
            full_address = f'{user.street_address} {user.city} {user.state_id} {user.zip_code}'
            g = geocoder.mapquest(full_address, key=MAPQUEST_API_KEY)
            if g.geojson['features'][0]['properties'].get('county'):
                county = g.geojson['features'][0]['properties'].get('county')
                user.county = county
            # resp = lob.USVerification.create(
            #     address=f'{user.street_address} {user.city} {user.state_id} {user.zip_code}')
            # if resp['components'].get('county'):
            #     county = resp['components']['county']
            #     user.county = county
            db.session.commit()
            return redirect(f'/users/{username}')
    return render_template('edit_user.html', form=form, user=user)


@ app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Deletes user from database and site"""
    curr_user = User.query.filter(
        User.username == session.get('username')).first()
    user = User.query.filter(User.username == username).first()
    if username == 'TestUser':
        flash ('Sorry, cannot delete Demo Account', 'danger')
        return redirect(f'/users/{username}')
    if session.get('username') != username:
        if curr_user.is_admin == True:
            deleted_user = User.query.filter(User.username == username).first()
            db.session.delete(deleted_user)
            db.session.commit()
            flash('User deleted', 'success')
            return redirect('/admin/users')
        else:
            flash('Must be logged in as user to delete', 'danger')
            return redirect('/')
    else:
        deleted_user = User.query.filter(User.username == username).first()
        db.session.delete(deleted_user)
        db.session.commit()
        session.pop('username')
        flash('User deleted', 'success')
        return redirect('/')
    
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = SendPasswordResetForm()
    if request.method == 'GET':
        return render_template('reset.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            user = User.verify_email(email)
            if user:
                send_email(user, SECRET_KEY)
            flash(
                f'Password Reset Link Emailed to {email}. Please check your Spam folder if you do not see it', 'success')
            return redirect('/login')


@app.route('/reset_password_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    """Password Reset Form for User"""
    user = User.verify_reset_token(token, SECRET_KEY)
    if not user:
        flash('No user found', 'danger')
        return redirect('/login')
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            password = form.password.data
            if password:
                user.change_password(password)
                flash('Password Successfully Changed', 'success')
                return redirect('/login')
    if 'username' in session:
        user = User.query.filter(
            User.username == session.get('username')).first()
        return render_template('reset_verified.html', user=user, form=form)
    return render_template('reset_verified.html', form=form)


def send_email(user, SECRET_KEY):
    """Sends Password Reset Email to User"""
    token = user.get_reset_token(SECRET_KEY)
    msg = Message()
    msg.subject = 'Voter Information Password Reset'
    msg.sender = ('Voter Info', 'voterinformationapp@gmail.com')
    msg.recipients = [user.email]
    url = url_for('reset_verified', token=token, _external=True)
    with app.open_resource('brand-img.png', 'rb') as fp:
        msg.attach('brand-img.png', "image/png", fp.read(),
                   headers=[['Content-ID', '<brandimg>'], ])
    msg.html = render_template('reset_email.html', url=url)
    mail.send(msg)