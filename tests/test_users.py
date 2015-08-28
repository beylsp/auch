from utils import AuchAppTest

class TestUsers(AuchAppTest):
    def test_get_token_wihout_login(self):
        response = self.test_app.get('/api/token')
        self.assertEquals(response.status, "401 UNAUTHORIZED")
