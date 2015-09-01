from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from functools import wraps
from flask_httpauth import HTTPBasicAuth
from auchapp.models import User
from flask import g
from flask import request
from auchapp import app

class RestHTTPBasicAuth(HTTPBasicAuth):

    def _verify_password(self, password, user):
        return pwd_context.verify(password, user.password_hash)

    def _verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

    def _check_http_auth(self):
        auth = request.authorization
        if auth:
            user = User.query.filter_by(username = auth.username).first()
        else:
            return False        
        if user and self._verify_password(auth.password, user):
            g.user = user
            return True                
        return False
    
    def _check_token(self):
        header_key = 'Authentication-Token'
        token = request.headers.get(header_key, None)
        if token:
            user = self._verify_auth_token(token)
            if user:
                g.user = user
                return True
        return False

    def http_auth_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if self._check_http_auth():
                return f(*args, **kwargs)
            else:
                return self.auth_error_callback()
        return decorated

    def auth_token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if self._check_token():
                return f(*args, **kwargs)
            else:
                return self.auth_error_callback()
        return decorated


auth = RestHTTPBasicAuth()