from auchapp import app
from utils import AuchAppTest
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import base64
import time
import json

class TestToken(AuchAppTest):
    
    def get_token(self, auth=None, **kwargs):
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + base64.b64encode('%s:%s' % auth)

        kwargs['headers'] = headers

        return self.test_app.open('/api/token', method='get', **kwargs)

    def get_token_wait(self, wait, auth=None, **kwargs):
        time.sleep(wait)
        return self.get_token(auth, **kwargs)
    
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

    def test_get_token_with_valid_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})
        
        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.get_token(headers = headers)        
        self.assertOk(response)

        json_response = json.loads(response.get_data())        
        self.assertEquals(json_response['token'], token)

    def test_get_token_with_expired_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 0.1)
        token = s.dumps({'id': 1})

        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.get_token_wait(wait = 1, headers = headers)
        self.assertNotAuthorized(response)

    def test_get_token_with_valid_token_but_user_removed(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})

        # delete user
        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.test_app.open('/api/users/delete', method='delete', headers = headers)
        self.assertOk(response)

        response = self.get_token(headers = headers)        
        self.assertNotAuthorized(response)


class TestNewUser(AuchAppTest):
 
    def test_new_user_with_no_json_header(self):
        response = self.test_app.post('/api/users')
        self.assertBadRequest(response)

    def test_new_user_with_no_json_body(self):
        response = self.jpost('/api/users')
        self.assertBadRequest(response)

    def test_new_user_with_empty_json_body(self):
        response = self.jpost('/api/users', data={})
        self.assertBadRequest(response)

    def test_new_user_with_no_user_and_no_password(self):
        response = self.jpost('/api/users', data={'username': '', 'password': ''})
        self.assertBadRequest(response)

    def test_new_user_with_user_and_no_password(self):
        response = self.jpost('/api/users', data = {'username': 'john'})
        self.assertBadRequest(response)

    def test_new_user_with_no_user_and_password(self):
        response = self.jpost('/api/users', data = {'password': 'doe'})
        self.assertBadRequest(response)

    def test_new_user_with_existing_user(self):
        response = self.jpost('/api/users', data = {'username': 'john', 'password': 'doe'})
        self.assertBadRequest(response)

    def test_new_user_with_user_password(self):
        response = self.jpost('/api/users', data = {'username': 'jane', 'password': 'roe'})
        self.assertCreated(response)

        user = self.get_user_from_db(id=2)
        self.assertEquals(user.username, 'jane')

class TestDelUser(AuchAppTest):

    def del_user(self, auth=None, **kwargs):
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + base64.b64encode('%s:%s' % auth)

        kwargs['headers'] = headers

        return self.test_app.open('/api/users/delete', method='delete', **kwargs)

    def del_user_wait(self, wait, auth=None, **kwargs):
        time.sleep(wait)
        return self.del_user(auth, **kwargs)

    def test_del_user_without_auth_header(self):
        response = self.del_user()
        self.assertNotAuthorized(response)

    def test_del_user_with_auth_header_but_missing_credentials(self):
        headers = {'Authorization' : 'Basic '}
        response = self.del_user(headers = headers)
        self.assertNotAuthorized(response)

    def test_del_user_with_digest_auth_header(self):
        headers = {'Authorization' : 'Digest ' + base64.b64encode('john:doe')}
        response = self.del_user(headers = headers)
        self.assertNotAuthorized(response)

    def test_del_user_with_invalid_auth_header(self):
        headers = {'Authorization' : 'Invalid ' + base64.b64encode('john:doe')}
        response = self.del_user(headers = headers)
        self.assertNotAuthorized(response)

    def test_del_user_with_invalid_user(self):
        response = self.del_user(auth=('joe', 'doe'))
        self.assertNotAuthorized(response)

    def test_del_user_with_invalid_password(self):
        response = self.del_user(auth=('john', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_del_user_with_invalid_user_and_password(self):
        response = self.del_user(auth=('joe', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_del_user_with_invalid_user_and_no_password(self):
        response = self.del_user(auth=('joe', ''))
        self.assertNotAuthorized(response)

    def test_del_user_with_valid_user_and_no_password(self):
        response = self.del_user(auth=('john', ''))
        self.assertNotAuthorized(response)

    def test_del_user_with_no_user_and_invalid_password(self):
        response = self.del_user(auth=('', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_del_user_with_no_user_and_valid_password(self):
        response = self.del_user(auth=('', 'doe'))
        self.assertNotAuthorized(response)

    def test_del_user_with_no_user_and_no_password(self):
        response = self.del_user(auth=('', ''))
        self.assertNotAuthorized(response)

    def test_del_user_with_login(self):
        response = self.del_user(auth=('john', 'doe'))
        self.assertOk(response)

        user = self.get_user_from_db(id=1)
        self.assertEquals(user, None)

    def test_del_user_with_valid_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})
        
        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.del_user(headers = headers)        
        self.assertOk(response)

        user = self.get_user_from_db(id=1)
        self.assertEquals(user, None)

    def test_del_user_with_expired_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 0.1)
        token = s.dumps({'id': 1})

        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.del_user_wait(wait = 1, headers = headers)
        self.assertNotAuthorized(response)
