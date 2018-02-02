"""Tests for the API."""

import copy
import unittest
from json import loads

from api.app import app
from api.utils import create_dropdb, dropdb
from api.config import local_test as CONFIG
from api.models import db, RiskTemplate, Insurer


class TestAPI(unittest.TestCase):
    """Tests for the API."""

    @classmethod
    def setUpClass(cls):
        """Create database and insert objects into the database"""
        app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DATABASE_URI
        app.testing = True

        with app.app_context():
            create_dropdb(CONFIG.SQLALCHEMY_DATABASE_URI)

    def _init_database(self):
        """Create Insurance and Risk templates."""
        # Create Insurers
        britecore = Insurer(name='BriteCore')
        vodafone = Insurer(name='Vodafone')
        dstv = Insurer(name='DSTV')

        db.session.add_all((britecore, vodafone, dstv))
        db.session.commit()

        # Create RiskTemplates
        automobile_insurance = RiskTemplate(
            insurer=britecore, name='Automobile',
            fields=[{'name': 'Price', 'dataType': 'currency'}]
        )

        phone_insurance = RiskTemplate(
            insurer=vodafone, name='Phone',
            fields=[
                {'name': 'Price', 'dataType': 'currency', 'value': 0},
                {'name': 'Plan', 'dataType': 'text', 'value': 'Pay as you Go'}
            ]
        )

        tv_insurance = RiskTemplate(
            insurer=dstv, name='Phone',
            fields=[
                {'name': 'Price', 'dataType': 'currency', 'value': 0},
                {
                    'name': 'Plan', 'dataType': 'enum',
                    'value': ['Compact', 'Superb', 'Premium']
                }
            ]
        )

        risk_templates = (
            automobile_insurance, phone_insurance, tv_insurance
        )

        db.session.add_all((risk_templates))
        db.session.commit()

        for risk_template in risk_templates:
            db.session.refresh(risk_template)

        self.automobile_insurance = automobile_insurance
        self.phone_insurance = phone_insurance
        self.tv_insurance = tv_insurance

    def setUp(self):
        """Setup app and test client."""
        self.client = app.test_client()  # Use a fresh client for each test
        with app.app_context():
            self._init_database()

    def test_risks(self):
        """Should return a list of risks in the expected format."""
        response = self.client.get('/risks/')

        expected = [
            {
                'id': self.automobile_insurance.id,
                'name': 'Automobile',
                'fields': [{'name': 'Price', 'dataType': 'currency'}]
            },
            {
                'id': self.phone_insurance.id,
                'name': 'Phone',
                'fields': [
                    {'name': 'Price', 'dataType': 'currency', 'value': 0},
                    {'name': 'Plan', 'dataType': 'text', 'value': 'Pay as you Go'}
                ]
            },
            {
                'id': self.tv_insurance.id,
                'name': 'Phone',
                'fields': [
                    {'name': 'Price', 'dataType': 'currency', 'value': 0},
                    {
                        'name': 'Plan', 'dataType': 'enum',
                        'value': ['Compact', 'Superb', 'Premium']
                    }
                ]
            }
        ]

        self.assertEqual(loads(response.data), expected)

    def test_risk(self):
        """Should return a single risk by id with all it's metadata."""
        response = self.client.get('/risks/%s/' % self.automobile_insurance.id)
        expected = {
            'id': self.automobile_insurance.id,
            'name': 'Automobile',
            'fields': [{'name': 'Price', 'dataType': 'currency'}]
        }

        self.assertEqual(loads(response.data), expected)

    def test_add_fields_on_the_fly(self):
        """
        A user should be able to create a record on the fly.

        And have it returned to them as JSON from the API
        """
        automobile_id = self.automobile_insurance.id

        # Add a new integer field "Accidents" to the Automobile insurance
        acc_field = {'name': 'Accidents', 'dataType': 'Integer', 'value': 0}
        with app.app_context():
            # SQLAlchemy has issues updating nested JSON so we have to fetch
            # the object again instead of reusing self.automobile_insurance
            auto_insurance = db.session.query(RiskTemplate).get(automobile_id)
            fields = copy.copy(auto_insurance.fields)
            fields.append(acc_field)

            auto_insurance.fields = fields
            db.session.commit()

        response = self.client.get('/risks/%s/' % self.automobile_insurance.id)
        expected = {
            'id': self.automobile_insurance.id,
            'name': 'Automobile',
            'fields': [
                {'name': 'Price', 'dataType': 'currency'},
                {'name': 'Accidents', 'dataType': 'Integer', 'value': 0}
            ]
        }

        self.assertEqual(loads(response.data), expected)

    def tearDown(self):
        """Clean all tables after each test completes."""
        with app.app_context():
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Drop database at the end of the test."""
        with app.app_context():
            dropdb(CONFIG.SQLALCHEMY_DATABASE_URI)


if __name__ == '__main__':
    unittest.main()
