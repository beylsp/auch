from utils import AuchAppTest

import base64
import json

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

    def test_sync_data_with_modifiedsince_header_RFC_1123(self):
        date = 'Sun, 06 Nov 1994 08:49:37 GMT'
        response = self.get_protected_resource(modified=date)
        self.assertOk(response)

    def test_sync_data_with_modifiedsince_header_RFC_1036(self):
        date = 'Sunday, 06-Nov-94 08:49:37 GMT'
        response = self.get_protected_resource(modified=date)
        self.assertOk(response)

    def test_sync_data_with_modifiedsince_header_ANSI_C(self):
        date = 'Sun Nov 6 08:49:37 1994'
        response = self.get_protected_resource(modified=date)
        self.assertOk(response)
