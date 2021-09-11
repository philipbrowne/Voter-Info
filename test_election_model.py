import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, State, Election, RegistrationRule, StateRegistrationRule

os.environ['DATABASE_URL'] = 'postgresql:///voter-test'
from app import app

db.create_all()

class ElectionModelTestCase(TestCase):
    """Test Election Model"""
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
        
    def test_election_model(self):
        ca = State(id='CA', name='California', capital='Sacramento')
        db.session.add(ca)
        db.session.commit()
        e = Election(name='Test Election', date='2022-01-01', state_id='CA')
        db.session.add(e)
        db.session.commit()
        self.assertEqual(e.name, 'Test Election')
        self.assertEqual(e.full_date, 'Saturday, January 1, 2022')
        self.assertEqual(e.state.name, 'California')
    
    def test_incomplete_election_model(self):
        ca = State(id='CA', name='California', capital='Sacramento')
        db.session.add(ca)
        db.session.commit()
        e1 = Election(name='Test Election', state_id='CA')
        db.session.add(e1)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        e2 = Election(date='2022-01-01', state_id='CA')
        db.session.add(e2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()