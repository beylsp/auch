import unittest
from auchapp import app

class TestUsers(unittest.TestCase):
    def test_get_token_wihout_login(self):
        self.test_app = app.test_client()
        response = self.test_app.get('/api/token')
        self.assertEquals(response.status, "401 UNAUTHORIZED")
