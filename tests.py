# from selenium import webdriver
import unittest

from server import app
from model import db, connect_to_db # example_data

from mini_seed import (load_users, load_friends, load_biz, load_userbiz,
                       load_promos, load_userpromos, load_checkin,
                       load_referrals, load_reviews, load_likes, load_invite)


class LoginRegisterTests(unittest.TestCase):
    """Tests for registration and log-in."""

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

    def test_no_register_yet(self):
        """Do users who haven't registered see the correct view?"""

        result = self.client.get('/register')
        self.assertIn('Business Account', result.data)
        self.assertNotIn('Profile', result.data)

    def test_register(self):
        """Do logged-in users see the correct view?"""

        register_info = {'fname': 'Pussy', 'lname': 'Galore',
                         'username': 'libellula', 'email': 'dragon@fly.com',
                         'pword': 'kissme'}

        result = self.client.post('/register', data=register_info,
                                  follow_redirects=True)

        self.assertIn('Profile', result.data)
        self.assertNotIn('Sign Up', result.data)

        # TO DO: Write tests for /pword-reset get and post.


class InfoTests(unittest.TestCase):
    """Tests for informational page(s)."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_about(self):
        """Can we reach the about page?"""

        result = self.client.get('/about-us')
        self.assertIn('Great things come in small packages', result.data)


class UserProfileTests(unittest.TestCase):
    """Tests for user page(s)."""

    def setUp(self):
        """Code to run before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_user_profile(self):
        """Can we reach the user profile page?"""

        result = self.client.get('/user-profile')

        self.assertIn('hunk', result.data)


class DatabaseTests(unittest.TestCase):
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
        # example_data()
        load_users()
        load_friends()
        load_biz()
        load_userbiz()
        load_promos()
        load_userpromos()
        load_checkin()
        load_referrals()
        load_reviews()
        load_likes()
        load_invite()

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
