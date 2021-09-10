from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class State(db.Model):
    """State Model"""
    __tablename__ = 'states'
    id = db.Column(db.String(2), primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    capital = db.Column(db.String(255), nullable=False)
    registration_url = db.Column(db.String(255))
    elections_url = db.Column(db.String(255))
    registration_in_person_deadline = db.Column(db.Text)
    registration_mail_deadline = db.Column(db.Text)
    registration_online_deadline = db.Column(db.Text)
    absentee_application_in_person_deadline = db.Column(db.Text)
    absentee_application_mail_deadline = db.Column(db.Text)
    absentee_application_online_deadline = db.Column(db.Text)
    voted_absentee_ballot_deadline = db.Column(db.Text)
    check_registration_url = db.Column(db.Text)
    polling_location_url = db.Column(db.Text)
    absentee_ballot_url = db.Column(db.Text)
    local_election_url = db.Column(db.Text)
    ballot_tracker_url = db.Column(db.Text)
    registration_rules = db.relationship(
        'RegistrationRule', secondary='state_registration_rules', backref='states')


class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String, nullable=False)
    city = db.Column(db.String(255), nullable=False)
    county = db.Column(db.String(255))
    state_id = db.Column(db.String(20), db.ForeignKey(
        'states.id', onupdate='CASCADE', ondelete='CASCADE'))
    zip_code = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    state = db.relationship('State', backref='users')
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now)

    @ classmethod
    def register(cls, username, password):
        """Register usedr with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(password)
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')
        # Return instance of user with username and hashed password
        return cls(username=username, password=hashed_utf8)

    @ classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct

        Return user if valid; otherwise return False.
        """
        # Queries for unique username from database
        user = User.query.filter_by(username=username).first()
        # If valid user and if password check lines up with database hash
        if user and bcrypt.check_password_hash(user.password, password):
            # Return User instance
            return user
        else:
            return False

    @property
    def registration_date(self):
        return self.created_at.strftime("%B %-d, %Y")


class Election(db.Model):
    """State Election model"""
    __tablename__ = 'elections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    state_id = db.Column(db.String(20), db.ForeignKey(
        'states.id', onupdate='CASCADE', ondelete='CASCADE'))
    state = db.relationship('State', backref='elections')

    @property
    def full_date(self):
        self.date.strftime('%A, %B %-d, %Y')


class RegistrationRule(db.Model):
    """Voter registration rule model"""
    __tablename__ = 'registration_rules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule = db.Column(db.Text, nullable=False, unique=True)


class StateRegistrationRule(db.Model):
    """Table linking Voter Registration Rule to State"""
    __tablename__ = 'state_registration_rules'
    state_id = db.Column(db.String(2), db.ForeignKey(
        'states.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey(
        'registration_rules.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
