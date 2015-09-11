from utils import AuchAppTest
from auchapp.store import store

import base64
import json
import random

class TestSync(AuchAppTest):

    def setUp(self):
        AuchAppTest.setUp(self)

        response = self.login()
        json_data = json.loads(response.data)
        self.token = json_data['token']

    def login(self):
        kwargs = {}
        headers = {'Authorization' : 'Basic ' + base64.b64encode('john:doe')}
        kwargs['headers'] = headers
        return self.test_app.open('/api/login', method='get', **kwargs)

    def get_protected_resource(self, modified=None, **kwargs):
        kwargs = {}
        headers = {'Authentication-Token' : self.token}
        kwargs['headers'] = headers
        if modified:
            headers['If-Modified-Since'] = modified
        
        return self.test_app.open('/api/sync', method='get', **kwargs)

    def test_sync_data_with_modifiedsince_header_missing(self):
        response = self.get_protected_resource()
        self.assertBadRequest(response)

    def test_sync_data_with_empty_modifiedsince_header(self):
        response = self.get_protected_resource(modified=' ')
        self.assertBadRequest(response)

    def test_sync_data_with_invalid_modifiedsince_header(self):
        date = '06-11-94'
        response = self.get_protected_resource(modified=date)
        self.assertBadRequest(response)

    def test_sync_data_with_modifiedsince_header_RFC_1123_and_sync_needed(self):
        date = 'Sun, 06 Nov 2014 08:49:37 GMT'
        store.set('last-update', 'Sun, 06 Aug 2015 08:49:37 GMT')
        response = self.get_protected_resource(modified=date)
        self.assertOk(response)

    def test_sync_data_with_modifiedsince_header_RFC_1123_and_not_modified(self):
        date = 'Sun, 06 Nov 2014 08:49:37 GMT'
        store.set('last-update', date)
        response = self.get_protected_resource(modified=date)
        self.assertNotModified(response)

    def test_sync_data_with_modifiedsince_header_RFC_1123_and_in_future(self):
        date = 'Sun, 06 Nov 2014 08:49:37 GMT'
        store.set('last-update', 'Sun, 06 Nov 2013 08:49:37 GMT')
        response = self.get_protected_resource(modified=date)
        self.assertBadRequest(response)

    def test_sync_data_with_modifiedsince_header_RFC_1036_and_sync_needed(self):
        date = 'Sunday, 06-Nov-14 08:49:37 GMT'
        store.set('last-update', 'Sunday, 06-Aug-15 08:49:37 GMT')
        response = self.get_protected_resource(modified=date)
        self.assertOk(response)

    def test_sync_data_with_modifiedsince_header_RFC_1036_and_not_modified(self):
        date = 'Sunday, 06-Nov-14 08:49:37 GMT'
        store.set('last-update', date)
        response = self.get_protected_resource(modified=date)
        self.assertNotModified(response)

    def test_sync_data_with_modifiedsince_header_RFC_1036_and_in_future(self):
        date = 'Sunday, 06-Nov-14 08:49:37 GMT'
        store.set('last-update', 'Sunday, 06-Nov-13 08:49:37 GMT')
        response = self.get_protected_resource(modified=date)
        self.assertBadRequest(response)

    def test_sync_data_with_modifiedsince_header_ANSI_C_and_sync_needed(self):
        date = 'Sun Nov 6 08:49:37 2014'
        store.set('last-update', 'Sun Aug 6 08:49:37 2015')
        response = self.get_protected_resource(modified=date)
        self.assertOk(response)

    def test_sync_data_with_modifiedsince_header_ANSI_C_and_not_modified(self):
        date = 'Sun Nov 6 08:49:37 2014'
        store.set('last-update', date)
        response = self.get_protected_resource(modified=date)
        self.assertNotModified(response)

    def test_sync_data_with_modifiedsince_header_ANSI_C_and_in_future(self):
        date = 'Sun Nov 6 08:49:37 2014'
        store.set('last-update', 'Sun Aug 6 08:49:37 2013')
        response = self.get_protected_resource(modified=date)
        self.assertBadRequest(response)

    def test_sync_data_with_modifiedsince_header_ANSI_C_but_no_token(self):
        self.token = ''
        date = 'Sun Nov 6 08:49:37 2014'
        response = self.get_protected_resource(modified=date)
        self.assertNotAuthorized(response)

    def test_sync_data_with_modifiedsince_header_RFC_1036_but_invalid_token(self):
        self.token = ''.join(random.sample(self.token, len(self.token)))
        date = 'Sunday, 06-Nov-14 08:49:37 GMT'
        response = self.get_protected_resource(modified=date)
        self.assertNotAuthorized(response)