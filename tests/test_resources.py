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

    def test_get_token_with_invalid_post_method(self):
        response = self.test_app.post('/api/login')
        self.assertNotAllowed(response)

    def test_get_token_with_invalid_patch_method(self):
        response = self.test_app.patch('/api/login')
        self.assertNotAllowed(response)

    def test_get_token_with_invalid_put_method(self):
        response = self.test_app.put('/api/login')
        self.assertNotAllowed(response)

    def test_get_token_with_invalid_delete_method(self):
        response = self.test_app.delete('/api/login')
        self.assertNotAllowed(response)

    def test_get_token_with_invalid_trace_method(self):
        response = self.test_app.trace('/api/login')
        self.assertNotAllowed(response)

    def test_get_test_resource_with_invalid_post_method(self):
        response = self.test_app.post('/api/test')
        self.assertNotAllowed(response)

    def test_get_test_resource_with_invalid_patch_method(self):
        response = self.test_app.patch('/api/test')
        self.assertNotAllowed(response)

    def test_get_test_resource_with_invalid_put_method(self):
        response = self.test_app.put('/api/test')
        self.assertNotAllowed(response)

    def test_get_test_resource_with_invalid_delete_method(self):
        response = self.test_app.delete('/api/test')
        self.assertNotAllowed(response)

    def test_get_test_resource_with_invalid_trace_method(self):
        response = self.test_app.trace('/api/test')
        self.assertNotAllowed(response)

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

    def test_del_user_with_invalid_get_method(self):
        response = self.test_app.get('/api/users/delete')
        self.assertNotAllowed(response)

    def test_del_user_with_invalid_post_method(self):
        response = self.test_app.post('/api/users/delete')
        self.assertNotAllowed(response)

    def test_del_user_with_invalid_patch_method(self):
        response = self.test_app.patch('/api/users/delete')
        self.assertNotAllowed(response)

    def test_del_user_with_invalid_head_method(self):
        response = self.test_app.head('/api/users/delete')
        self.assertNotAllowed(response)

    def test_del_user_with_invalid_put_method(self):
        response = self.test_app.put('/api/users/delete')
        self.assertNotAllowed(response)

    def test_del_user_with_invalid_trace_method(self):
        response = self.test_app.trace('/api/users/delete')
        self.assertNotAllowed(response)

    def test_edit_user_with_invalid_get_method(self):
        response = self.test_app.get('/api/users/edit')
        self.assertNotAllowed(response)

    def test_edit_user_with_invalid_post_method(self):
        response = self.test_app.post('/api/users/edit')
        self.assertNotAllowed(response)

    def test_edit_user_with_invalid_patch_method(self):
        response = self.test_app.patch('/api/users/edit')
        self.assertNotAllowed(response)

    def test_edit_user_with_invalid_head_method(self):
        response = self.test_app.head('/api/users/edit')
        self.assertNotAllowed(response)

    def test_edit_user_with_invalid_delete_method(self):
        response = self.test_app.delete('/api/users/edit')
        self.assertNotAllowed(response)

    def test_edit_user_with_invalid_trace_method(self):
        response = self.test_app.trace('/api/users/edit')
        self.assertNotAllowed(response)
