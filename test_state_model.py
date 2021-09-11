from app import app
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, State, Election, RegistrationRule, StateRegistrationRule

os.environ['DATABASE_URL'] = 'postgresql://voter-test'

db.drop_all()
db.create_all()

class StateModelTestCase(TestCase):
    """Test State Model"""
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
        
    def test_state_model(self):
        """Tests Creation of New State Model"""
        california = State(id='CA', name='California', capital='Sacramento',
           registration_url='https://registertovote.ca.gov/', elections_url='https://www.sos.ca.gov/elections', registration_in_person_deadline='15 days before Election Day.', registration_mail_deadline='Postmarked 15 days before Election Day.', registration_online_deadline='15 days before Election Day.', check_registration_url='https://www.sos.ca.gov/elections/registration-status/', polling_location_url='http://www.sos.ca.gov/elections/polling-place/', absentee_ballot_url='https://www.sos.ca.gov/elections/voter-registration/vote-mail', local_election_url='https://www.sos.ca.gov/elections/voting-resources/county-elections-offices/', ballot_tracker_url='https://www.sos.ca.gov/elections/ballot-status/', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='If you need to change where your ballot is mailed, submit address change at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked by Election Day and received no later than 17 days after the Election.')
        db.session.add(california)
        db.session.commit()
        self.assertEqual(len(california.users), 0)
        self.assertEqual(len(california.elections), 0)
        self.assertEqual(california.registration_url, 'https://registertovote.ca.gov/')
        self.assertEqual(california.name, 'California')
        self.assertEqual(california.capital, 'Sacramento')
        self.assertEqual(repr(california), f'<State {california.id} {california.name}>')
    
    def test_user_state(self):
        """Tests Association Between User and State"""
        california = State(id='CA', name='California', capital='Sacramento',
           registration_url='https://registertovote.ca.gov/', elections_url='https://www.sos.ca.gov/elections', registration_in_person_deadline='15 days before Election Day.', registration_mail_deadline='Postmarked 15 days before Election Day.', registration_online_deadline='15 days before Election Day.', check_registration_url='https://www.sos.ca.gov/elections/registration-status/', polling_location_url='http://www.sos.ca.gov/elections/polling-place/', absentee_ballot_url='https://www.sos.ca.gov/elections/voter-registration/vote-mail', local_election_url='https://www.sos.ca.gov/elections/voting-resources/county-elections-offices/', ballot_tracker_url='https://www.sos.ca.gov/elections/ballot-status/', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='If you need to change where your ballot is mailed, submit address change at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked by Election Day and received no later than 17 days after the Election.')
        db.session.add(california)
        db.session.commit()
        u1 = User(username='TEST_USER', password='TEST_HASHED_PW', first_name='TEST_FIRST', last_name='TEST_LAST', street_address='TEST_STREET_ADDRESS', city='TEST_CITY', state_id='CA', zip_code='21046', email='TESTEMAIL@test.com')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.state.name, 'California')
        self.assertEqual(u1.state.capital, 'Sacramento')
        self.assertEqual(u1.state.elections_url, 'https://www.sos.ca.gov/elections')
        self.assertEqual(u1.state.registration_online_deadline, '15 days before Election Day.')
    
    def test_duplicate_state(self):
        """Tests Creation of Non-Unique Values State ID and Name"""
        california = State(id='CA', name='California', capital='Sacramento')
        db.session.add(california)
        db.session.commit()
        dupe_cal_1 = State(id='CA', name='Dupe_Name', capital='Dupe_Capital')
        db.session.add(dupe_cal_1)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        dupe_cal_2 = State(id='AA', name='California', capital='Dupe_Capital')
        db.session.add(dupe_cal_2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
    
    def test_incomplete_state(self):
        """Tests Creation of Incomplete State Model missing Required Values"""
        incomplete_cal_1 = State(id='CA', name='California')
        db.session.add(incomplete_cal_1)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        incomplete_cal_2 = State(id='CA', capital='Sacramento')
        db.session.add(incomplete_cal_2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        incomplete_cal_3 = State(name='CA', capital='Sacramento')
        db.session.add(incomplete_cal_3)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()