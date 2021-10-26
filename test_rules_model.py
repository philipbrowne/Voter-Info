from app import app
import os
from unittest import TestCase

from models import db, User, State, Election, RegistrationRule, StateRegistrationRule

os.environ['DATABASE_URL'] = 'postgresql://voter-test'

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

    def test_rules_model(self):
        """Tests Registration Rules Model"""
        ca = State(id='CA', name='California', capital='Sacramento')
        db.session.add(ca)
        db.session.commit()
        r1 = RegistrationRule(rule='TEST_RULE')
        db.session.add(r1)
        db.session.commit()
        self.assertEqual(r1.rule, 'TEST_RULE')
        sr1 = StateRegistrationRule(state_id='CA', rule_id=r1.id)
        db.session.add(sr1)
        db.session.commit()
        self.assertEqual(r1.states[0].name, 'California')
        self.assertEqual(ca.registration_rules[0].rule, 'TEST_RULE')
