import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, State, Election, RegistrationRule, StateRegistrationRule

os.environ['DATABASE_URL'] = 'postgresql://voter-test'
from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test User Model"""
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
    
    def test_user_model(self):
        california = State(id='CA', name='California', capital='Sacramento',
           registration_url='https://registertovote.ca.gov/', elections_url='https://www.sos.ca.gov/elections', registration_in_person_deadline='15 days before Election Day.', registration_mail_deadline='Postmarked 15 days before Election Day.', registration_online_deadline='15 days before Election Day.', check_registration_url='https://www.sos.ca.gov/elections/registration-status/', polling_location_url='http://www.sos.ca.gov/elections/polling-place/', absentee_ballot_url='https://www.sos.ca.gov/elections/voter-registration/vote-mail', local_election_url='https://www.sos.ca.gov/elections/voting-resources/county-elections-offices/', ballot_tracker_url='https://www.sos.ca.gov/elections/ballot-status/', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='If you need to change where your ballot is mailed, submit address change at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked by Election Day and received no later than 17 days after the Election.')
        db.session.add(california)
        db.session.commit()
        u1 = User(username='TEST_USER', password='TEST_HASHED_PW', first_name='TEST_FIRST', last_name='TEST_LAST', street_address='TEST_STREET_ADDRESS', city='TEST_CITY', state_id='CA', zip_code='21046', email='TESTEMAIL@test.com')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.username, 'TEST_USER')
        self.assertEqual(u1.first_name, 'TEST_FIRST')
        self.assertEqual(u1.street_address, 'TEST_STREET_ADDRESS')
        self.assertEqual(u1.state.name, 'California')
        self.assertEqual(repr(u1), '<User TEST_USER TEST_FIRST TEST_LAST>')
    
    def test_user_register(self):
        california = State(id='CA', name='California', capital='Sacramento')
        db.session.add(california)
        db.session.commit()
        u1 = User(username='TEST_USER', password='TEST_HASHED_PW', first_name='TEST_FIRST', last_name='TEST_LAST', street_address='TEST_STREET_ADDRESS', city='TEST_CITY', county='TEST_COUNTY', state_id='CA', zip_code='21046', email='TESTEMAIL@test.com')
        u3 = u1.register(u1.username, u1.password, u1.first_name, u1.last_name, u1.street_address, u1.city, u1.county, u1.state_id, u1.zip_code, u1.email)
        db.session.commit()
        self.assertNotEqual(u1.password, u3.password)
    
    def test_duplicate_user(self):
        california = State(id='CA', name='California', capital='Sacramento')
        db.session.add(california)
        db.session.commit()
        u1 = User(username='TEST_USER', password='TEST_HASHED_PW', first_name='TEST_FIRST', last_name='TEST_LAST', street_address='TEST_STREET_ADDRESS', city='TEST_CITY', state_id='CA', zip_code='21046', email='TESTEMAIL@test.com')
        u1 = u1.register(u1.username, u1.password, u1.first_name, u1.last_name, u1.street_address, u1.city, u1.county, u1.state_id, u1.zip_code, u1.email)
        db.session.add(u1)
        db.session.commit()
        dupe1 = User(username='TEST_USER', password='DUPE_HASHED_PW', first_name='DUPE_FIRST', last_name='DUPE_LAST', street_address='DUPE_STREET_ADDRESS', city='DUPE_CITY', state_id='CA', zip_code='21046', email='DUPEEMAIL@test.com')
        db.session.add(dupe1)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        dupe2 = User(username='UNIQUE_USER', password='UNIQUE_HASHED_PW', first_name='UNIQUE_FIRST', last_name='UNIQUE_LAST', street_address='UNIQUE_STREET_ADDRESS', city='UNIQUE_CITY', state_id='CA', zip_code='21046', email='TESTEMAIL@test.com')
        db.session.add(dupe2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        
    def test_user_login(self):
        california = State(id='CA', name='California', capital='Sacramento')
        db.session.add(california)
        db.session.commit()
        u1 = User(username='TEST_USER', password='TEST_HASHED_PW', first_name='TEST_FIRST', last_name='TEST_LAST', street_address='TEST_STREET_ADDRESS', city='TEST_CITY', county='TEST_COUNTY', state_id='CA', zip_code='21046', email='TESTEMAIL@test.com')
        db.session.add(u1)
        db.session.commit()
        db.session.delete(u1)
        db.session.commit()
        u2 = u1.register(u1.username, u1.password, u1.first_name, u1.last_name, u1.street_address, u1.city, u1.county, u1.state_id, u1.zip_code, u1.email)
        db.session.commit()
        self.assertEqual(u2.authenticate(u2.username, u1.password), u2)
        self.assertFalse(u2.authenticate(u2.username, 'WRONG_PASSWORD'))

        
        
        