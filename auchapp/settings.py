import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'auch.db') +
                               '?check_same_thread=False')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
