from utils import AuchAppTest
import base64

class TestUsers(AuchAppTest):
    
    def get_token(self, auth=None, **kwargs):
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + base64.b64encode('%s:%s' % auth)

        kwargs['headers'] = headers

        return self.test_app.open('/api/token', method='get', **kwargs)
    
    def test_get_token_wihout_login(self):
        response = self.get_token()
        self.assertNotAuthorized(response)

    def test_get_token_with_invalid_user(self):
        response = self.get_token(auth=('joe', 'doe'))
        self.assertNotAuthorized(response)

    def test_get_token_with_invalid_password(self):
        response = self.get_token(auth=('john', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_get_token_with_invalid_user_and_password(self):
        response = self.get_token(auth=('joe', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_get_token_with_login(self):
        response = self.get_token(auth=('john', 'doe'))
        self.assertOk(response)
        