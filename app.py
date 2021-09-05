from flask import Flask, render_template, request, redirect, session, flash, jsonify, abort, send_from_directory, url_for, json
import json

from forms import NewUserForm, UserLoginForm
from models import connect_db, db, User

from sqlalchemy.exc import IntegrityError
import os

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
        if form.apartment_number.data:
            apartment_number = form.apartment_number.data
        else:
            apartment_number = 'N/A'
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        date_of_birth = form.date_of_birth.data
        new_user = User(username=username, password=password,
                        email=email, )
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors = ['Sorry - that username is already taken!']
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash(f'Welcome {new_user.username}!', 'success')
        return redirect(f'/users/{new_user.username}')
    return render_template('register.html', form=form)
