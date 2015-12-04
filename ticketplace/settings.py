"""settings.py

Note: All sensitive information should be configured at the deployment site
"""

import os


class Config(object):
    """ Default configurations for all.
    """
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'suuuper secret key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres@localhost/ticketplace'


class ProductionConfig(Config):
    """ Configuration for Azure. Not yet configured
    """
    CACHE_TYPE = 'simple'


class HerokuConfig(Config):
    """ Heroku server configuration used in wsgi.py
    """
    CACHE_TYPE = 'simple'


class DevelopmentConfig(Config):
    """ Development configuration for local development
    """
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True


class TestConfig(Config):
    """ Test configuration for local py.test
    """
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL') or 'postgresql://postgres@localhost/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False


class TravisConfig(TestConfig):
    """ Test configuration for and travis-ci
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/test'
