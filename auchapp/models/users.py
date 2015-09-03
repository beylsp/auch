from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from passlib.apps import custom_app_context as pwd_context
from marshmallow import Schema
from marshmallow import fields
from marshmallow import ValidationError
from marshmallow import validates
from auchapp import app
from auchapp.database import db

import datetime as dt

class User(db.Model):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(28), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    created_at = dt.datetime.now()

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id})
    
    def __repr__(self):
        return '<id %r, user %r, password %r>' % (self.id, self.username, self.password)


class UserSchema(Schema):

    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates('username')
    def validate_username(self, username):
        if not username:
            raise ValidationError('Invalid user name.')
        if User.query.filter_by(username = username).first() is not None:
            raise ValidationError('User already exists.')

    @validates('password')
    def validate_password(self, password):
        if not password:
            raise ValidationError('Invalid password.')

    def make_object(self, data):
        if 'password' in data:
            hash = pwd_context.encrypt(data['password'])
            data.update({'password' : hash })
        return data


user_schema = UserSchema()