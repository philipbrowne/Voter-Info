from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String, nullable=False)
    apartment_number = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    @classmethod
    def register(cls, username, password):
        """Register usedr with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(password)
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')
        # Return instance of user with username and hashed password
        return cls(username=username, password=hashed_utf8)

    @classmethod
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
