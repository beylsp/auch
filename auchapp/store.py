from flask_redis import FlaskRedis
from auchapp import app
redis_store = FlaskRedis(app)
