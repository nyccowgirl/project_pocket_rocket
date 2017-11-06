import unittest

from server import app
from model import db, example_data, connect_to_db


class BuddyTests(unittest.TestCase):
    """Tests for the BUDdy site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get('/')
        self.assertIn('Paying it forward', result.data)

    def test_no_login_yet(self):
        """Do users who haven't logged in see the correct view?"""

        result = self.client.get('/')
        self.assertIn('Log In', result.data)
        self.assertNotIn('Profile', result.data)

    def test_login(self):
        """Do logged-in users see the correct view?"""

        login_info = {'username': 'libellula', 'email': 'dragon@fly.com'}

        result = self.client.post('/login', data=login_info,
                                  follow_redirects=True)

        self.assertIn('Profile', result.data)
        self.assertNotIn('Log In', result.data)


class BuddyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    # def test_games(self):
    #     """Test departments page."""

    #     result = self.client.get("/games")
    #     self.assertIn("Power Grid", result.data)


if __name__ == "__main__":
    unittest.main()
