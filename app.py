from flask import Flask, render_template, request, redirect, session, flash, jsonify, abort, send_from_directory, url_for, json
from flask_mail import Mail, Message
import json
import easypost
from api_keys import LOB_API_KEY, GOOGLE_CIVIC_API_KEY, MAPQUEST_API_KEY, EASYPOST_API_KEY
from secret_keys import MAIL_USERNAME, MAIL_PASSWORD
import requests
import geocoder

from forms import NewUserForm, UserLoginForm, EditUserForm, SendPasswordResetForm, ResetPasswordForm, StateEditForm, StateRegistrationRuleForm, ElectionForm, AdminUserForm
from models import connect_db, db, User, State, Election, RegistrationRule

from sqlalchemy.exc import IntegrityError
import os
import lob
lob.api_key = LOB_API_KEY
easypost.api_key = EASYPOST_API_KEY


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
SECRET_KEY = app.config['SECRET_KEY']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
mail = Mail(app)

connect_db(app)


@app.route('/favicon.ico')
def favicon():
    """Returns Favicon"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    """Landing Page"""
    if 'username' in session:
        user = User.query.filter(User.username == session['username']).first()
        return render_template('index.html', user=user)
    return render_template('index.html')

# These Routes are User Registration/Profile/Login Related


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

# These Routes are For Application Content


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

# The following Routes are for Administrator Use


@app.route('/admin')
def admin_index():
    """Index page for Administrator"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    return render_template('admin_index.html', user=curr_user)


@app.route('/admin/users')
def admin_show_user_list():
    """Shows user list to those with administrator access"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    users = User.query.order_by(User.last_name).all()
    return render_template('admin_users.html', users=users, user=curr_user)


@app.route('/admin/users/<username>/edit', methods=['GET', 'POST'])
def admin_edit_user(username):
    """Admin site to edit specific user"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    user = User.query.get_or_404(username)
    form = AdminUserForm()
    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.password.data = user.password
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.street_address.data = user.street_address
        form.city.data = user.city
        form.state_id.data = user.state_id
        form.zip_code.data = user.zip_code
        form.is_admin.data = user.is_admin
        return render_template('admin_edit_user.html', user=user, form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            password = form.password.data
            user.username = form.username.data
            user.street_address = form.street_address.data
            user.city = form.city.data
            user.state_id = form.state_id.data
            user.zip_code = form.zip_code.data
            user.is_admin = form.is_admin.data
            full_address = f'{user.street_address} {user.city} {user.state_id} {user.zip_code}'
            g = geocoder.mapquest(full_address, key=MAPQUEST_API_KEY)
            if g.geojson['features'][0]['properties'].get('county'):
                county = g.geojson['features'][0]['properties'].get('county')
                user.county = county
            if password:
                user.change_password(password)
            flash(f'Changed information for {user.username}', 'success')
            return redirect('/admin/users')


@app.route('/admin/states')
def admin_show_states():
    """Show List of States In Admin Mode with Links to Each State"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    states = State.query.all()
    return render_template('admin_states.html', user=curr_user, states=states)


@app.route('/admin/states/<state_id>')
def admin_show_state_info(state_id):
    """Admin Page for State Information"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    state = State.query.get_or_404(state_id)
    return render_template('admin_state_info.html', state=state, user=curr_user)


@app.route('/admin/states/<state_id>/edit', methods=['GET', 'POST'])
def admin_edit_state_info(state_id):
    """Admin Page to Edit State Info"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    state = State.query.get_or_404(state_id)
    form = StateEditForm()
    if request.method == 'GET':
        form.registration_url.data = state.registration_url
        form.elections_url.data = state.elections_url
        form.registration_in_person_deadline.data = state.registration_in_person_deadline
        form.registration_mail_deadline.data = state.registration_mail_deadline
        form.registration_online_deadline.data = state.registration_online_deadline
        form.absentee_application_in_person_deadline.data = state.absentee_application_in_person_deadline
        form.absentee_application_mail_deadline.data = state.absentee_application_mail_deadline
        form.absentee_application_online_deadline.data = state.absentee_application_online_deadline
        form.voted_absentee_ballot_deadline.data = state.voted_absentee_ballot_deadline
        form.check_registration_url.data = state.check_registration_url
        form.polling_location_url.data = state.polling_location_url
        form.absentee_ballot_url.data = state.absentee_ballot_url
        form.local_election_url.data = state.local_election_url
        form.ballot_tracker_url.data = state.ballot_tracker_url
        return render_template('admin_state_edit.html', state=state, form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            state.registration_url = form.registration_url.data
            state.elections_url = form.elections_url.data
            state.registration_in_person_deadline = form.registration_in_person_deadline.data
            state.registration_mail_deadline = form.registration_mail_deadline.data
            state.registration_online_deadline = form.registration_online_deadline.data
            state.absentee_application_in_person_deadline = form.absentee_application_in_person_deadline.data
            state.absentee_application_mail_deadline = form.absentee_application_mail_deadline.data
            state.absentee_application_online_deadline = form.absentee_application_online_deadline.data
            state.voted_absentee_ballot_deadline = form.voted_absentee_ballot_deadline.data
            state.check_registration_url = form.check_registration_url.data
            state.polling_location_url = form.polling_location_url.data
            state.absentee_ballot_url = form.absentee_ballot_url.data
            state.local_election_url = form.local_election_url.data
            state.ballot_tracker_url = form.ballot_tracker_url.data
            db.session.commit()
            flash(f'Changed Information for {state.name}', 'success')
            return redirect(f'/admin/{state.id}')


@app.route('/admin/state/<state_id>/rules/<int:rule_id>/delete', methods=['POST'])
def remove_rule_from_state(state_id, rule_id):
    """Removes a Voter Registration Rule from a state"""
    state = State.query.get_or_404(state_id)
    rule = RegistrationRule.query.get_or_404(rule_id)
    state.registration_rules.remove(rule)
    db.session.commit()
    flash(f'Removed rule from {state.name}', 'success')
    return redirect(f'/admin/states/{state_id}')


@app.route('/admin/rules')
def admin_show_registration_rules():
    """Shows Admin Page for Voter Registration Rules"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    rules = RegistrationRule.query.all()
    return render_template('admin_rules.html', user=curr_user, rules=rules)


@app.route('/admin/rules/new', methods=['GET', 'POST'])
def admin_add_registration_rule():
    """Admin Feature - Add new Voter Registration Rule"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    states = State.query.all()
    form = StateRegistrationRuleForm()
    if request.method == 'POST':
        new_rule = RegistrationRule(rule=form.rule.data)
        db.session.add(new_rule)
        db.session.commit()
        state_list = list(request.form.listvalues())[2:]
        new_rule.states.clear()
        for item in state_list:
            new_rule.states.append(State.query.get(item[0]))
        db.session.commit()
        flash(f'Voter Registration Rule Added', 'success')
        return redirect('/admin/rules')
    if request.method == 'GET':
        return render_template('admin_new_rule.html', states=states, user=curr_user, form=form)


@app.route('/admin/rules/<int:rule_id>/edit', methods=['GET', 'POST'])
def admin_edit_registration_rule(rule_id):
    """Admin Feature - Edit Voter Registration Rule"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    edit_rule = RegistrationRule.query.get_or_404(rule_id)
    form = StateRegistrationRuleForm()
    states = State.query.all()
    if request.method == 'GET':
        form.rule.data = edit_rule.rule
        return render_template('admin_edit_reg_rule.html', form=form, rule=edit_rule, user=curr_user, states=states)
    if request.method == 'POST':
        edit_rule.rule = form.rule.data
        state_list = list(request.form.listvalues())[2:]
        edit_rule.states.clear()
        for item in state_list:
            edit_rule.states.append(State.query.get(item[0]))
        db.session.commit()
        flash('Successfully changed rule', 'success')
        return redirect('/admin/rules')


@app.route('/admin/rules/<int:rule_id>/delete', methods=['POST'])
def admin_delete_registration_rule(rule_id):
    """Admin Feature - Delete Voter Registration Rule"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    deleted_rule = RegistrationRule.query.get_or_404(rule_id)
    db.session.delete(deleted_rule)
    db.session.commit()
    flash(f'Registration Rule deleted', 'success')
    return redirect('/admin/rules')


@app.route('/admin/elections')
def admin_show_elections():
    """Admin Feature - Show lists of all elections in each state"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    elections = Election.query.order_by(Election.state_id, Election.date).all()
    return render_template('admin_elections.html', user=curr_user, elections=elections)


@app.route('/admin/elections/new', methods=['GET', 'POST'])
def admin_new_election():
    """Admin Feature Adding New Election"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    form = ElectionForm()
    if form.validate_on_submit():
        name = form.name.data
        state_id = form.state_id.data
        date = form.date.data
        new_election = Election(name=name, date=date, state_id=state_id)
        db.session.add(new_election)
        db.session.commit()
        flash(
            f'Election added on {new_election.full_date} in {new_election.state.name}', 'success')
        return redirect('/admin/elections')
    return render_template('admin_new_election.html', user=curr_user, form=form)


@app.route('/admin/elections/<int:election_id>/edit', methods=['GET', 'POST'])
def admin_edit_election(election_id):
    """Admin Feature - Edit Election Information"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    form = ElectionForm()
    election = Election.query.get_or_404(election_id)
    if request.method == 'GET':
        form.name.data = election.name
        form.date.data = election.date
        form.state_id.data = election.state_id
        return render_template('admin_edit_election.html', user=curr_user, election=election, form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            election.name = form.name.data
            election.date = form.date.data
            election.state_id = form.state_id.data
            db.session.commit()
            flash(
                f'Election on {election.full_date} in {election.state.name} successfully changed', 'success')
            return redirect('/admin/elections')


@app.route('/admin/elections/<int:election_id>/delete', methods=['POST'])
def admin_delete_election(election_id):
    """Admin Feature - Delete Election"""
    if 'username' not in session:
        flash('Please sign in first', 'danger')
        return redirect('/')
    curr_user = User.query.get(session['username'])
    if curr_user.is_admin == False:
        flash('Cannot access page', 'danger')
        return redirect('/')
    deleted_election = Election.query.filter(
        Election.id == election_id).first()
    db.session.delete(deleted_election)
    db.session.commit()
    flash(f'Election deleted', 'success')
    return redirect('/admin/elections')
