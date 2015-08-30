import unittest
import tempfile
import os

from auchapp import app
from auchapp.models import db
from auchapp.models import User

class AuchAppTest(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:////%s' % app.config['DATABASE'],
            SECRET_KEY = os.urandom(24)
        )
        
        # create db and populate
        db.create_all()
        user = User(username='john')
        user.hash_password(password='doe')
        db.session.add(user)
        db.session.commit()

        # create a test app every test case can use.
        self.test_app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def assertStatusCode(self, response, status_code):
        """Assert the status code of a Flask test client response."""
        self.assertEquals(response.status_code, status_code)
        return response

    def assertOk(self, response):
        """Test that response status code is 200."""
        return self.assertStatusCode(response, 200)

    def assertNotAuthorized(self, response):
        """Test that response status code is 401."""
        return self.assertStatusCode(response, 401)