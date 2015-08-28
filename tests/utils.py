import unittest
from auchapp import app

class AuchAppTest(unittest.TestCase):
    def setUp(self):
        # create a test app every test case can use.
        self.test_app = app.test_client()
