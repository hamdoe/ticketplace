#! ../env/bin/python
# -*- coding: utf-8 -*-
from ticketplace import create_app


class TestConfig:
    def test_development_config(self):
        """ Tests if the development config loads correctly """

        app = create_app('DevelopmentConfig', env='development')

        assert app.config['DEBUG'] is True
        assert app.config['CACHE_TYPE'] == 'null'

    def test_test_config(self):
        """ Tests if the test config loads correctly """

        app = create_app('TestConfig', env='development')

        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_ECHO'] is True
        assert app.config['CACHE_TYPE'] == 'null'

    def test_heroku_config(self):
        """ Tests if the heroku config loads correctly """

        app = create_app('HerokuConfig', env='production')

        assert app.config['CACHE_TYPE'] == 'simple'

    def test_production_config(self):
        """ Tests if the production config loads correctly """

        app = create_app('ProductionConfig', env='production')

        assert app.config['CACHE_TYPE'] == 'simple'
