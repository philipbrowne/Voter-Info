import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, State, Election, RegistrationRule, StateRegistrationRule

os.environ['DATABASE_URL'] = 'postgresql://voter-test'
from app import app

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ViewTestCase(TestCase):
        def setUp(self):
            """Create test client, add sample data."""
            State.query.delete()
            User.query.delete()
            Election.query.delete()
            RegistrationRule.query.delete()
            StateRegistrationRule.query.delete()
            self.client = app.test_client()
            self.test_state = State(id='CA', name='California', capital='Sacramento')
            db.session.add(self.test_state)
            db.session.commit()
            self.testuser = User.register(username='TEST_NAME', password='TEST_PW', first_name='TEST_FIRST', last_name='TEST_LAST', street_address='200 N Spring St', city='Los Angeles', county='Los Angeles', state_id='CA', zip_code='90012', email='test@test.com')
            db.session.commit()
            self.test_election = Election(name='Test Election', date='2022-01-01', state_id='CA')
            db.session.add(self.test_election)
            db.session.commit()
            self.test_rule = RegistrationRule(rule='TEST_RULE')
            db.session.add(self.test_rule)
            db.session.commit()
            self.test_state_reg_rule = StateRegistrationRule(state_id='CA', rule_id=self.test_rule.id)
            db.session.add(self.test_state_reg_rule)
            db.session.commit()
        
        def tearDown(self):
            """Clean up any fouled DB transactions"""
            db.session.rollback()
        
        def test_home_page(self):
            """Test home page before being logged in"""
            with self.client as c:
                resp = c.get('/')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Easily register', html)
        def test_user_login(self):
            """Tests User Login Page"""
            with self.client as c:
                resp = c.post('/login', data={
                    'username' : 'TEST_NAME',
                    'password' : 'TEST_PW'
                }, follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Welcome back', html)
                self.assertIn('Voting Information', html)
                self.assertIn('Officials', html)
            with self.client as c:
                resp = c.post('/login', data={
                    'username' : 'TEST_NAME1',
                    'password' : 'TEST_PW'
                }, follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Invalid', html)
            with self.client as c:
                resp = c.post('/login', data={
                    'username' : 'TEST_NAME',
                    'password' : 'TEST_PW1'
                }, follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Invalid', html)        
        def test_elections_page(self):
            """Tests State Elections Page"""
            with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = self.testuser.username
                resp = c.get('/elections')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Elections in California', html)
        def test_voter_info_page(self):
            """Tests State Voter Info Page"""
            with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = self.testuser.username
                resp = c.get('/state-information')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('California', html)
        def test_public_officials_page(self):
            with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = self.testuser.username
                resp = c.get('/officials')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('President of', html)
        def test_profile_page(self):
            """Tests Viewing User Profile"""
            with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = self.testuser.username
                resp = c.get(f'/users/{self.testuser.username}')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Street Address', html)
        def test_edit_user_page(self):
            """Tests Editing User Profile"""
            with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = self.testuser.username
                resp = c.get(f'/users/{self.testuser.username}/edit')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Street Address', html)
                resp = c.post(f'/users/{self.testuser.username}/edit', data={
                    'first_name': 'NEW_FIRST_NAME',
                    'last_name' :'NEW_LAST_NAME',
                    'street_address': self.testuser.street_address,
                    'city': self.testuser.city,
                    'state_id': self.testuser.state_id,
                    'zip_code': self.testuser.zip_code
                })
                self.assertEqual(resp.status_code, 302)
                resp = c.post(f'/users/{self.testuser.username}/edit', data={
                    'first_name': 'NEW_FIRST_NAME',
                    'last_name' :'NEW_LAST_NAME',
                    'street_address': self.testuser.street_address,
                    'city': self.testuser.city,
                    'state_id': self.testuser.state_id,
                    'zip_code': self.testuser.zip_code
                }, follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('NEW_FIRST_NAME', html)
                self.assertIn('NEW_LAST_NAME', html)
        def test_register_page(self):
            """Tests User Registration"""
            with self.client as c:
                resp = c.get('/register')
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                resp = c.post('/register', data={
                    'username' : 'NEW_TEST_USER',
                    'password' : 'NEW_TEST_PASSWORD',
                    'email' : 'test2@test.com',
                    'first_name' : 'NEW_TEST_FIRST',
                    'last_name' : 'NEW_TEST_LAST',
                    'street_address' : '200 N SPRING ST',
                    'city' : 'Los Angeles',
                    'state_id' : 'CA',
                    'zip_code' : '90012' 
                }, follow_redirects=True)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn('Welcome NEW_TEST_USER!', html)
        def test_logout_page(self):
            """Tests Logging out of Page"""
            with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = self.testuser.username
                resp = c.get('/logout')
                self.assertEqual(resp.status_code, 302)
            with self.client as c:
                with c.session_transaction() as session:
                    session['username'] = self.testuser.username
                resp = c.get('/logout', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('has logged out.', html)
            with self.client as c:
                resp = c.get('/logout', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('Please sign', html)
        