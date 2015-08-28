import unittest
from auchapp import app

class AuchAppTest(unittest.TestCase):
    def setUp(self):
        # create a test app every test case can use.
        self.test_app = app.test_client()

    def assertStatusCode(self, response, status_code):
        self.assertEquals(response.status_code, status_code)
        return response

    def assertNotAuthorized(self, response):
        return self.assertStatusCode(response, 401)