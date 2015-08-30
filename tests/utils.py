import unittest
import tempfile
import os
import json

from auchapp import app
from auchapp.models import db
from auchapp.models import User
from passlib.apps import custom_app_context as pwd_context

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

    def jpost(self, endpoint, data=None, **kwargs):
        if data:
            data = json.dumps(data)

        headers = kwargs.get('headers', {})
        headers['Content-Type'] = 'application/json'
        kwargs['headers'] = headers

        return self.test_app.open(endpoint, method='post', data=data, **kwargs)

    def get_user_from_db(self, id):
        return User.query.get(id)

    def assertStatusCode(self, response, status_code):
        """Assert the status code of a Flask test client response."""
        self.assertEquals(response.status_code, status_code)
        return response

    def assertOk(self, response):
        """Test that response status code is 200."""
        return self.assertStatusCode(response, 200)

    def assertCreated(self, response):
        """Test that response status code is 201."""
        return self.assertStatusCode(response, 201)

    def assertBadRequest(self, response):
        """Test that response status code is 400."""
        return self.assertStatusCode(response, 400)

    def assertNotAuthorized(self, response):
        """Test that response status code is 401."""
        return self.assertStatusCode(response, 401)
    
    def assertNotFound(self, response):
        """Test that response status code is 404."""
        return self.assertStatusCode(response, 404)

    def assertNotAllowed(self, response):
        """Test that response status code is 405."""
        return self.assertStatusCode(response, 405)
