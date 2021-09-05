from flask import Flask, render_template, request, redirect, session, flash, jsonify, abort, send_from_directory, url_for, json
import json
from api_keys import LOB_API_KEY, GOOGLE_CIVIC_API_KEY
import requests

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
    print(request.json)
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
    print(response_info)
    return 'Hi!'


{'normalizedInput': {'line1': '13161 Brayton Drive', 'city': 'Anchorage', 'state': 'AK', 'zip': '99516'}, 'kind': 'civicinfo#representativeInfoResponse', 'divisions': {'ocd-division/country:us': {'name': 'United States', 'officeIndices': [0, 1]}, 'ocd-division/country:us/state:ak': {'name': 'Alaska', 'officeIndices': [2, 3, 4, 5, 6, 7]}, 'ocd-division/country:us/state:ak/borough:anchorage': {'name': 'Anchorage Municipality', 'alsoKnownAs': ['ocd-division/country:us/state:ak/place:anchorage'], 'officeIndices': [8]}}, 'offices': [{'name': 'President of the United States', 'divisionId': 'ocd-division/country:us', 'levels': ['country'], 'roles': ['headOfGovernment', 'headOfState'], 'officialIndices': [0]}, {'name': 'Vice President of the United States', 'divisionId': 'ocd-division/country:us', 'levels': ['country'], 'roles': ['deputyHeadOfGovernment'], 'officialIndices': [1]}, {'name': 'U.S. Senator', 'divisionId': 'ocd-division/country:us/state:ak', 'levels': ['country'], 'roles': ['legislatorUpperBody'], 'officialIndices': [2, 3]}, {'name': 'U.S. Representative', 'divisionId': 'ocd-division/country:us/state:ak', 'levels': ['country'], 'roles': ['legislatorLowerBody'], 'officialIndices': [4]}, {'name': 'Governor of Alaska', 'divisionId': 'ocd-division/country:us/state:ak', 'levels': ['administrativeArea1'], 'roles': ['headOfGovernment'], 'officialIndices': [5]}, {'name': 'Lieutenant Governor of Alaska', 'divisionId': 'ocd-division/country:us/state:ak', 'levels': ['administrativeArea1'], 'roles': ['deputyHeadOfGovernment'], 'officialIndices': [6]}, {'name': 'AK Supreme Court Justice', 'divisionId': 'ocd-division/country:us/state:ak', 'levels': ['administrativeArea1'], 'roles': ['judge'], 'officialIndices': [7, 8, 9, 10, 11]}, {'name': 'AK Court of Appeals Judge', 'divisionId': 'ocd-division/country:us/state:ak', 'levels': ['administrativeArea1'], 'roles': ['judge'], 'officialIndices': [12, 13, 14]}, {'name': 'Mayor of Anchorage', 'divisionId': 'ocd-division/country:us/state:ak/borough:anchorage', 'levels': ['administrativeArea2'], 'roles': ['headOfGovernment'], 'officialIndices': [15]}], 'officials': [{'name': 'Joseph R. Biden', 'address': [{'line1': '1600 Pennsylvania Avenue Northwest', 'city': 'Washington', 'state': 'DC', 'zip': '20500'}], 'party': 'Democratic Party', 'phones': ['(202) 456-1111'], 'urls': ['https://www.whitehouse.gov/'], 'channels': [{'type': 'Twitter', 'id': 'potus'}]}, {'name': 'Kamala D. Harris', 'address': [{'line1': '1600 Pennsylvania Avenue Northwest', 'city': 'Washington', 'state': 'DC', 'zip': '20500'}], 'party': 'Democratic Party', 'phones': ['(202) 456-1111'], 'urls': ['https://www.whitehouse.gov/'], 'channels': [{'type': 'Twitter', 'id': 'VP'}]}, {'name': 'Dan Sullivan', 'address': [{'line1': '302 Hart Senate Office Building', 'city': 'Washington', 'state': 'DC', 'zip': '20510'}], 'party': 'Republican Party', 'phones': ['(202) 224-3004'], 'urls': ['https://www.sullivan.senate.gov/'], 'photoUrl': 'http://bioguide.congress.gov/bioguide/photo/S/S001198.jpg', 'channels': [{'type': 'Facebook', 'id': 'SenDanSullivan'}, {'type': 'Twitter', 'id': 'SenDanSullivan'}, {'type': 'YouTube', 'id': 'UC7tXCm8gKlAhTFo2kuf5ylw'}]}, {'name': 'Lisa Murkowski', 'address': [{'line1': '522 Hart Senate Office Building', 'city': 'Washington', 'state': 'DC', 'zip': '20510'}], 'party': 'Republican Party', 'phones': [
    '(202) 224-6665'], 'urls': ['https://www.murkowski.senate.gov/'], 'photoUrl': 'http://bioguide.congress.gov/bioguide/photo/M/M001153.jpg', 'channels': [{'type': 'Facebook', 'id': 'SenLisaMurkowski'}, {'type': 'Twitter', 'id': 'lisamurkowski'}, {'type': 'YouTube', 'id': 'senatormurkowski'}]}, {'name': 'Don Young', 'address': [{'line1': '2314 Rayburn House Office Building', 'city': 'Washington', 'state': 'DC', 'zip': '20515'}], 'party': 'Republican Party', 'phones': ['(202) 225-5765'], 'urls': ['https://donyoung.house.gov/'], 'photoUrl': 'http://donyoung.house.gov/UploadedFiles/PressKit/DY-Official_Photo.jpg', 'channels': [{'type': 'Facebook', 'id': 'RepDonYoung'}, {'type': 'Twitter', 'id': 'repdonyoung'}, {'type': 'YouTube', 'id': 'RepDonYoung'}]}, {'name': 'Mike Dunleavy', 'party': 'Republican Party', 'phones': ['(907) 465-3500'], 'urls': ['https://gov.alaska.gov/'], 'channels': [{'type': 'Facebook', 'id': 'GovDunleavy'}, {'type': 'Twitter', 'id': 'GovDunleavy'}]}, {'name': 'Kevin Meyer', 'party': 'Republican Party', 'phones': ['(907) 465-3520'], 'urls': ['https://ltgov.alaska.gov/'], 'channels': [{'type': 'Facebook', 'id': 'LtGovMeyer'}, {'type': 'Twitter', 'id': 'ltgovmeyer'}]}, {'name': 'Daniel E. Winfree', 'address': [{'line1': '303 K Street', 'city': 'Anchorage', 'state': 'AK', 'zip': '99501'}], 'party': 'Nonpartisan', 'phones': ['(907) 264-0612'], 'urls': ['http://courts.alaska.gov/judges/']}, {'name': 'Dario Borghesan', 'address': [{'line1': '303 K Street', 'city': 'Anchorage', 'state': 'AK', 'zip': '99501'}], 'party': 'Nonpartisan', 'phones': ['(907) 264-0612'], 'urls': ['http://courts.alaska.gov/judges/']}, {'name': 'Peter J. Maassen', 'address': [{'line1': '303 K Street', 'city': 'Anchorage', 'state': 'AK', 'zip': '99501'}], 'party': 'Nonpartisan', 'phones': ['(907) 264-0612'], 'urls': ['http://courts.alaska.gov/judges/']}, {'name': 'Susan M. Carney', 'address': [{'line1': '303 K Street', 'city': 'Anchorage', 'state': 'AK', 'zip': '99501'}], 'party': 'Nonpartisan', 'phones': ['(907) 264-0612'], 'urls': ['http://courts.alaska.gov/judges/']}, {'name': 'VACANT', 'address': [{'line1': '303 K Street', 'city': 'Anchorage', 'state': 'AK', 'zip': '99501'}], 'party': 'Nonpartisan', 'phones': ['(907) 264-0612'], 'urls': ['http://courts.alaska.gov/judges/']}, {'name': 'Bethany S. Harbison', 'address': [{'line1': '303 K Street', 'city': 'Anchorage', 'state': 'AK', 'zip': '99501'}], 'party': 'Nonpartisan', 'phones': ['(907) 264-0612'], 'urls': ['http://courts.alaska.gov/judges/']}, {'name': 'Marjorie K. Allard', 'address': [{'line1': '303 K Street', 'city': 'Anchorage', 'state': 'AK', 'zip': '99501'}], 'party': 'Nonpartisan', 'phones': ['(907) 264-0612'], 'urls': ['http://courts.alaska.gov/judges/']}, {'name': 'Tracey Wollenberg', 'address': [{'line1': '303 K Street', 'city': 'Anchorage', 'state': 'AK', 'zip': '99501'}], 'party': 'Nonpartisan', 'phones': ['(907) 264-0612'], 'urls': ['http://courts.alaska.gov/judges/']}, {'name': 'David Bronson', 'address': [{'line1': '632 West 6th Avenue', 'city': 'Anchorage', 'state': 'AK', 'zip': '99501'}], 'party': 'Nonpartisan', 'phones': ['(907) 343-7177'], 'urls': ['http://www.muni.org/Departments/Mayor/Pages/default.aspx'], 'emails': ['dave.bronson@anchorageak.gov'], 'channels': [{'type': 'Facebook', 'id': 'MayorDaveBronson'}, {'type': 'Twitter', 'id': 'MayorBronson'}]}]}
