from app import app
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, State, Election, RegistrationRule, StateRegistrationRule

os.environ['DATABASE_URL'] = 'postgresql://voter-test'

db.drop_all()
db.create_all()

class RulesModelTestCase(TestCase):
    """Test Rules Model"""
    def setUp(self):
        """Create test client, add sample data."""
        State.query.delete()
        User.query.delete()
        Election.query.delete()
        RegistrationRule.query.delete()
        StateRegistrationRule.query.delete()
        self.client = app.test_client()
    
    def tearDown(self):
        """Clean up any fouled DB transactions"""
        db.session.rollback()
        
    
        