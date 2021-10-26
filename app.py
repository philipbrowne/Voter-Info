from flask import Flask, render_template, session, send_from_directory
from flask_mail import Mail

import easypost
from models import connect_db, User

import os
import lob


app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')

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

URI = os.environ.get('DATABASE_URL', 'postgresql:///voter-db')
if URI.startswith("postgres://"):
    URI = URI.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get(
    'SECRET_KEY', SECRET_KEY)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
lob.api_key = LOB_API_KEY
easypost.api_key = EASYPOST_API_KEY
mail = Mail(app)

connect_db(app)

import views_user
import views_information
import views_admin


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
