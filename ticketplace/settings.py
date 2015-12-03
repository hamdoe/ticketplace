import os


class Config(object):
    SECRET_KEY = 'secret key'


class ProductionConfig(Config):
    """ Configuration for Azure. Not yet configured
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    CACHE_TYPE = 'simple'


class HerokuConfig(Config):
    """ Heroku server configuration used in wsgi.py
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    CACHE_TYPE = 'simple'


class DevelopmentConfig(Config):
    """ Development configuration for local development
    """
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:h@110w0r1d@localhost/ticketplace'

    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True


class TestConfig(Config):
    """ Test configuration for local py.test and travis-ci
    """
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://test:testpassword@localhost/test'

    SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
