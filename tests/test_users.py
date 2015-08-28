import unittest
from app import app

class TestUsers(unittest.TestCase):
    def test_get_token_wihout_login(self):
        self.test_app = app.test_client()
