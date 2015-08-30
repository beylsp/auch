from utils import AuchAppTest

class TestResources(AuchAppTest):

    def test_get_resource_not_found(self):
        response = self.test_app.get('/api/doesnotexist')
        self.assertNotFound(response)

    def test_patch_resource_not_found(self):
        response = self.test_app.patch('/api/doesnotexist')
        self.assertNotFound(response)

    def test_post_resource_not_found(self):
        response = self.test_app.post('/api/doesnotexist')
        self.assertNotFound(response)

    def test_head_resource_not_found(self):
        response = self.test_app.head('/api/doesnotexist')
        self.assertNotFound(response)

    def test_put_resource_not_found(self):
        response = self.test_app.put('/api/doesnotexist')
        self.assertNotFound(response)

    def test_delete_resource_not_found(self):
        response = self.test_app.delete('/api/doesnotexist')
        self.assertNotFound(response)

    def test_options_resource_not_found(self):
        response = self.test_app.options('/api/doesnotexist')
        self.assertNotFound(response)

    def test_trace_resource_not_found(self):
        response = self.test_app.trace('/api/doesnotexist')
        self.assertNotFound(response)

    def test_new_user_with_invalid_get_method(self):
        response = self.test_app.get('/api/users')
        self.assertNotAllowed(response)

    def test_new_user_with_invalid_patch_method(self):
        response = self.test_app.patch('/api/users')
        self.assertNotAllowed(response)

    def test_new_user_with_invalid_head_method(self):
        response = self.test_app.head('/api/users')
        self.assertNotAllowed(response)

    def test_new_user_with_invalid_put_method(self):
        response = self.test_app.put('/api/users')
        self.assertNotAllowed(response)

    def test_new_user_with_invalid_delete_method(self):
        response = self.test_app.delete('/api/users')
        self.assertNotAllowed(response)

    def test_new_user_with_invalid_trace_method(self):
        response = self.test_app.trace('/api/users')
        self.assertNotAllowed(response)

