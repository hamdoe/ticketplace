"""settings.py

Note: All sensitive information should be configured at the deployment site
"""

import os


class Config(object):
    """ Default configurations for all.
    """
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'suuuper secret key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres@localhost/ticketplace'

    # For uploading files (Optional)
    AWS_KEY = os.environ.get('AWS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

    #: ids for contents to display on frontpage
    FRONTPAGE_CONTENT_IDS = []

    #: Helpdesk
    HELPDESK_EMAIL = 'help@ticketplace.net'

class ProductionConfig(Config):
    """ Configuration for Azure. Not yet configured
    """
    CACHE_TYPE = 'simple'


class HerokuConfig(Config):
    """ Heroku server configuration used in wsgi.py
    """
    FRONTPAGE_CONTENT_IDS = [3, 61, 51, 56, 1, 2]
    CACHE_TYPE = 'simple'


class DevelopmentConfig(Config):
    """ Development configuration for local development
    """
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True

    FRONTPAGE_CONTENT_IDS = [3, 45, 43, 48, 1, 38]


class TestConfig(Config):
    """ Test configuration for local py.test
    """
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL') or 'postgresql://postgres@localhost/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False


class TravisConfig(TestConfig):
    """ Test configuration for and travis-ci
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/test'


# Load local configuration files
try:
    from ticketplace.local_settings import *
except ImportError:
    pass