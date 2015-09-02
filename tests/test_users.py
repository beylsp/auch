from auchapp import app
from utils import AuchAppTest
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passlib.apps import custom_app_context as pwd_context
import base64
import time
import json

class TestLogin(AuchAppTest):
    
    def login(self, auth=None, **kwargs):
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + base64.b64encode('%s:%s' % auth)

        kwargs['headers'] = headers

        return self.test_app.open('/api/login', method='get', **kwargs)

    def login_wait(self, wait, auth=None, **kwargs):
        time.sleep(wait)
        return self.login(auth, **kwargs)
    
    def test_login_wihout_auth_header(self):
        response = self.login()
        self.assertNotAuthorized(response)

    def test_login_with_auth_header_but_missing_credentials(self):
        headers = {'Authorization' : 'Basic '}
        response = self.login(headers = headers)
        self.assertNotAuthorized(response)

    def test_login_with_digest_auth_header(self):
        headers = {'Authorization' : 'Digest ' + base64.b64encode('john:doe')}
        response = self.login(headers = headers)
        self.assertNotAuthorized(response)

    def test_login_with_invalid_auth_header(self):
        headers = {'Authorization' : 'Invalid ' + base64.b64encode('john:doe')}
        response = self.login(headers = headers)
        self.assertNotAuthorized(response)

    def test_login_with_incomplete_auth_header(self):
        headers = {'Authorization' : base64.b64encode('john:doe')}
        response = self.login(headers = headers)
        self.assertNotAuthorized(response)

    def test_login_with_invalid_user(self):
        response = self.login(auth=('joe', 'doe'))
        self.assertNotAuthorized(response)

    def test_login_with_invalid_password(self):
        response = self.login(auth=('john', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_login_with_invalid_user_and_password(self):
        response = self.login(auth=('joe', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_login_with_invalid_user_and_no_password(self):
        response = self.login(auth=('joe', ''))
        self.assertNotAuthorized(response)

    def test_login_with_valid_user_and_no_password(self):
        response = self.login(auth=('john', ''))
        self.assertNotAuthorized(response)

    def test_login_with_no_user_and_invalid_password(self):
        response = self.login(auth=('', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_login_with_no_user_and_valid_password(self):
        response = self.login(auth=('', 'doe'))
        self.assertNotAuthorized(response)

    def test_login_with_no_user_and_no_password(self):
        response = self.login(auth=('', ''))
        self.assertNotAuthorized(response)

    def test_login_with_credentials(self):
        response = self.login(auth=('john', 'doe'))
        self.assertOk(response)

        json_data = json.loads(response.data)
        self.assertIn('token', json_data)

    def test_login_with_user_removed(self):
        self.del_user_from_db(id=1)
        response = self.login(auth=('john', 'doe'))
        self.assertNotAuthorized(response)


class TestProtectedResource(TestLogin):
    
    def setUp(self):
        AuchAppTest.setUp(self)

        response = self.login(auth=('john', 'doe'))
        json_data = json.loads(response.data)
        self.token = json_data['token']
        
    def test_get_protected_resource_with_valid_token(self):
        response = self.get_protected_resource(endpoint='/api/test', token=self.token)
        self.assertOk(response)

        json_data = json.loads(response.data)
        self.assertIn('success', json_data['result'])

    def test_get_protected_resource_with_invalid_token(self):
        token = 'ayJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MTIxMzc3OCwiaWF0IjoxNDQxMjEzMTc4fQ.eyJpZCI6MX0.Gr-lwQ8uQhw4N9hyCdh2gsplZx4UFN5dHpf90Uy9OYQ' 
        response = self.get_protected_resource(endpoint='/api/test', token=token)
        self.assertNotAuthorized(response)
 
    def test_get_protected_resource_with_expired_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 0.1)
        token = s.dumps({'id': 1}) 

        response = self.get_protected_resource_wait(wait=1, endpoint='/api/test', token=token)
        self.assertNotAuthorized(response)
 
    def test_get_protected_resource_with_valid_token_but_user_removed(self):
        self.del_user(id=1) 
        response = self.get_protected_resource(endpoint='/api/test', token=self.token)
        self.assertNotAuthorized(response)

    def test_get_protected_resource_wihout_auth_header_key(self):
        kwargs = { 'headers' : {} }
        response = self.test_app.open('/api/test', method='get', **kwargs)
        self.assertNotAuthorized(response)

    def test_get_protected_resource_with_auth_header_but_missing_token(self):
        kwargs = { 'headers' : {'Authentication-Token' : ''} }
        response = self.test_app.open('/api/test', method='get', **kwargs)
        self.assertNotAuthorized(response)

    def test_get_protected_resource_with_invalid_auth_header(self):
        kwargs = { 'headers' : {'Token-Authentication' : self.token} }
        response = self.test_app.open('/api/test', method='get', **kwargs)
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


class TestDelUser(TestLogin):

    def setUp(self):
        AuchAppTest.setUp(self)

        response = self.login(auth=('john', 'doe'))
        json_data = json.loads(response.data)
        self.token = json_data['token']

    def del_user(self, token=None, **kwargs):
        headers = kwargs.get('headers', {})
        if token:
            headers['Authentication-Token'] = token

        kwargs['headers'] = headers

        return self.test_app.open('/api/users/delete', method='delete', **kwargs)

    def del_user_wait(self, wait, token=None, **kwargs):
        time.sleep(wait)
        return self.del_user(token, **kwargs)

    def test_del_user_without_auth_header_key(self):
        response = self.del_user()
        self.assertNotAuthorized(response)

    def test_del_user_with_auth_header_but_missing_token(self):
        headers = {'Authentication-Token' : ''}
        response = self.del_user(headers = headers)
        self.assertNotAuthorized(response)

    def test_del_user_with_invalid_auth_token(self):
        token = 'ayJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MTIxMzc3OCwiaWF0IjoxNDQxMjEzMTc4fQ.eyJpZCI6MX0.Gr-lwQ8uQhw4N9hyCdh2gsplZx4UFN5dHpf90Uy9OYQ' 
        headers = {'Token-Authentication' : token}
        response = self.del_user(headers = headers)
        self.assertNotAuthorized(response)

    def test_del_user_with_valid_token(self):
        response = self.del_user(self.token)
        self.assertOk(response)

        user = self.get_user_from_db(id=1)
        self.assertEquals(user, None)

    def test_del_user_with_expired_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in=0.1)
        token = s.dumps({'id': 1})

        response = self.del_user_wait(wait=1, token=token)
        self.assertNotAuthorized(response)


class TestEditUser(AuchAppTest):
    
    def edit_user(self, auth=None, **kwargs):
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + base64.b64encode('%s:%s' % auth)

        kwargs['headers'] = headers

        return self.test_app.open('/api/users/edit', method='put', **kwargs)

    def edit_user_wait(self, wait, auth=None, **kwargs):
        time.sleep(wait)
        return self.edit_user(auth, **kwargs)

    def test_edit_user_without_auth_header(self):
        response = self.edit_user()
        self.assertNotAuthorized(response)

    def test_edit_user_with_auth_header_but_missing_credentials(self):
        headers = {'Authorization' : 'Basic '}
        response = self.edit_user(headers = headers)
        self.assertNotAuthorized(response)

    def test_edit_user_with_digest_auth_header(self):
        headers = {'Authorization' : 'Digest ' + base64.b64encode('john:doe')}
        response = self.edit_user(headers = headers)
        self.assertNotAuthorized(response)

    def test_edit_user_with_invalid_auth_header(self):
        headers = {'Authorization' : 'Invalid ' + base64.b64encode('john:doe')}
        response = self.edit_user(headers = headers)
        self.assertNotAuthorized(response)

    def test_edit_user_with_invalid_user(self):
        response = self.edit_user(auth=('joe', 'doe'))
        self.assertNotAuthorized(response)

    def test_edit_user_with_invalid_password(self):
        response = self.edit_user(auth=('john', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_edit_user_with_invalid_user_and_password(self):
        response = self.edit_user(auth=('joe', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_edit_user_with_invalid_user_and_no_password(self):
        response = self.edit_user(auth=('joe', ''))
        self.assertNotAuthorized(response)

    def test_edit_user_with_valid_user_and_no_password(self):
        response = self.edit_user(auth=('john', ''))
        self.assertNotAuthorized(response)

    def test_edit_user_with_no_user_and_invalid_password(self):
        response = self.edit_user(auth=('', 'bloggs'))
        self.assertNotAuthorized(response)

    def test_edit_user_with_no_user_and_valid_password(self):
        response = self.edit_user(auth=('', 'doe'))
        self.assertNotAuthorized(response)

    def test_edit_user_with_no_user_and_no_password(self):
        response = self.edit_user(auth=('', ''))
        self.assertNotAuthorized(response)

    def test_edit_user_with_login_and_no_json_header(self):
        response = self.edit_user(auth=('john', 'doe'))
        self.assertBadRequest(response)

    def test_edit_user_with_token_and_no_json_header(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})
        
        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.edit_user(headers = headers)        
        self.assertBadRequest(response)

    def test_edit_user_with_login_and_no_json_body(self):
        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        response = self.jput('/api/users/edit', headers=headers)
        self.assertBadRequest(response)

    def test_edit_user_with_token_and_no_json_body(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})
        
        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.jput('/api/users/edit', headers = headers)        
        self.assertBadRequest(response)

    def test_edit_user_with_login_and_empty_json_body(self):
        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        response = self.jput('/api/users/edit', data={}, headers=headers)
        self.assertBadRequest(response)

    def test_edit_user_with_token_and_empty_json_body(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})
        
        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.jput('/api/users/edit', data={}, headers = headers)        
        self.assertBadRequest(response)

    def test_edit_user_with_login_and_edit_with_empty_username(self):
        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        response = self.jput('/api/users/edit', data={'username': ''}, headers=headers)
        self.assertBadRequest(response)

    def test_edit_user_with_token_and_edit_with_empty_username(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})

        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.jput('/api/users/edit', data={'username': ''}, headers=headers)
        self.assertBadRequest(response)

    def test_edit_user_with_login_and_edit_with_empty_password(self):
        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        response = self.jput('/api/users/edit', data={'password': ''}, headers=headers)
        self.assertBadRequest(response)

    def test_edit_user_with_token_and_edit_with_empty_password(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})

        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.jput('/api/users/edit', data={'password': ''}, headers=headers)
        self.assertBadRequest(response)

    def test_edit_user_with_login_and_edit_with_empty_username_and_password(self):
        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        response = self.jput('/api/users/edit', data={'username': '', 'password': ''}, headers=headers)
        self.assertBadRequest(response)

    def test_edit_user_with_token_and_edit_with_empty_username_and_password(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})

        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.jput('/api/users/edit', data={'username': '', 'password': ''}, headers=headers)
        self.assertBadRequest(response)

    def test_edit_user_with_login_and_edit_with_valid_username(self):
        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        response = self.jput('/api/users/edit', data={'username': 'jane'}, headers=headers)
        self.assertOk(response)

        user = self.get_user_from_db(id=1)
        self.assertEquals(user.username, 'jane')

    def test_edit_user_with_token_and_edit_with_valid_username(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})

        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.jput('/api/users/edit', data={'username': 'jane'}, headers=headers)
        self.assertOk(response)

        user = self.get_user_from_db(id=1)
        self.assertEquals(user.username, 'jane')

    def test_edit_user_with_login_and_edit_with_valid_password(self):
        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        response = self.jput('/api/users/edit', data={'password': 'roe'}, headers=headers)
        self.assertOk(response)

        user = self.get_user_from_db(id=1)
        self.assertTrue(pwd_context.verify('roe', user.password_hash))
    
    def test_edit_user_with_token_and_edit_with_valid_password(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})

        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.jput('/api/users/edit', data={'password': 'roe'}, headers=headers)
        self.assertOk(response)

        user = self.get_user_from_db(id=1)
        self.assertTrue(pwd_context.verify('roe', user.password_hash))

    def test_edit_user_with_login_and_edit_with_valid_username_and_password(self):
        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        response = self.jput('/api/users/edit', data={'username': 'jane', 'password': 'roe'}, headers=headers)
        self.assertOk(response)

        user = self.get_user_from_db(id=1)
        self.assertEquals(user.username, 'jane')
        self.assertTrue(pwd_context.verify('roe', user.password_hash))

    def test_edit_user_with_token_and_edit_with_valid_username_and_password(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})

        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.jput('/api/users/edit', data={'username': 'jane', 'password': 'roe'}, headers=headers)
        self.assertOk(response)

        user = self.get_user_from_db(id=1)
        self.assertEquals(user.username, 'jane')
        self.assertTrue(pwd_context.verify('roe', user.password_hash))

    def test_edit_user_with_login_and_edit_with_invalid_username(self):
        self.add_user_to_db('jane', 'roe')

        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        response = self.jput('/api/users/edit', data={'username': 'jane'}, headers=headers)
        self.assertBadRequest(response)

    def test_edit_user_with_token_and_edit_with_invalid_username(self):
        self.add_user_to_db('jane', 'roe')

        s = Serializer(app.config['SECRET_KEY'], expires_in = 600)
        token = s.dumps({'id': 1})

        encoded = base64.b64encode('%s:' % token)
        headers = {'Authorization' : 'Basic ' + encoded}
        response = self.jput('/api/users/edit', data={'username': 'jane'}, headers=headers)
        self.assertBadRequest(response)
