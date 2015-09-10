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
        response = self.get_protected_resource(endpoint='/api/sync')
        self.assertBadRequest(response)
