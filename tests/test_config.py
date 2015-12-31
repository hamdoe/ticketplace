#! ../env/bin/python
# -*- coding: utf-8 -*-
from ticketplace import create_app


class TestConfig:
    def test_development_config(self):
        """ Tests if the development config loads correctly """

        app = create_app('ticketplace.settings.DevelopmentConfig')

        assert app.config['DEBUG'] is True
        assert app.config['CACHE_TYPE'] == 'null'

    def test_test_config(self):
        """ Tests if the test config loads correctly """

        app = create_app('ticketplace.settings.TestConfig')

        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_ECHO'] is False
        assert app.config['CACHE_TYPE'] == 'null'

    def test_heroku_config(self):
        """ Tests if the heroku config loads correctly """

        app = create_app('ticketplace.settings.HerokuConfig')

        assert app.config['CACHE_TYPE'] == 'simple'

    def test_production_config(self):
        """ Tests if the production config loads correctly """

        app = create_app('ticketplace.settings.ProductionConfig')

        assert app.config['CACHE_TYPE'] == 'simple'
