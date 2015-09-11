from flask_redis import FlaskRedis
from auchapp import app
from datetime import datetime as dt

import werkzeug


class RedisStoreFactory(object):
    def __new__(cls, class_name, parents, attributes):
        if app.testing:            
            from mockredis import MockRedis
            c = type(class_name, (MockRedis,), attributes)
        else:
            c = type(class_name, (FlaskRedis,), attributes)            
        return c

        
class Store(object):
    __metaclass__ = RedisStoreFactory

    @property
    def last_update(self):
        last_update = werkzeug.http.parse_date(self.get('last-update'))        
        if last_update:
            return last_update
        return dt(1970, 1, 1)

store = Store()