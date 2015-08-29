from utils import AuchAppTest
import base64

class TestUsers(AuchAppTest):
    
    def get_token(self, auth=None, **kwargs):
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + base64.b64encode('%s:%s' % auth)

        kwargs['headers'] = headers

        return self.test_app.open('/api/token', method='get', **kwargs)
    
    def test_get_token_wihout_auth_header(self):
        response = self.get_token()
        self.assertNotAuthorized(response)

    def test_get_token_with_auth_header_but_missing_credentials(self):
        headers = {'Authorization' : 'Basic '}
        response = self.get_token(headers = headers)
        self.assertNotAuthorized(response)

    def test_get_token_with_digest_auth_header(self):
        headers = {'Authorization' : 'Digest ' + base64.b64encode('john:doe')}
        response = self.get_token(headers = headers)
        self.assertNotAuthorized(response)

    def test_get_token_with_invalid_auth_header(self):
        headers = {'Authorization' : 'Invalid ' + base64.b64encode('john:doe')}
        response = self.get_token(headers = headers)
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

    def test_get_token_with_invalid_user_and_no_password(self):
        response = self.get_token(auth=('joe', ''))
        self.assertNotAuthorized(response)

    def test_get_token_with_valid_user_and_no_password(self):
        response = self.get_token(auth=('john', ''))
        self.assertNotAuthorized(response)

    def test_get_token_with_no_user_and_invalid_password(self):
        response = self.get_token(auth=('', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_get_token_with_no_user_and_valid_password(self):
        response = self.get_token(auth=('', 'doe'))
        self.assertNotAuthorized(response)

    def test_get_token_with_no_user_and_no_password(self):
        response = self.get_token(auth=('', ''))
        self.assertNotAuthorized(response)

    def test_get_token_with_login(self):
        response = self.get_token(auth=('john', 'doe'))
        self.assertOk(response)
        