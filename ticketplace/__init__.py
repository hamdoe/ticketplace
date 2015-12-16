#! ../env/bin/python
# -*- coding: utf-8 -*-
from flask.ext.admin.contrib.sqla.view import ModelView
from ticketplace.controllers.admin import CompanyView, ContentView

__author__ = 'Minjune Kim'
__email__ = 'june@ticketplace.net'
__version__ = '0.1'

from flask import Flask
from flask.ext.admin.base import Admin
from flask.ext.bootstrap import Bootstrap
from webassets.loaders import PythonLoader as PythonAssetsLoader

from ticketplace.controllers.main import main
from ticketplace.controllers.eduticket import eduticket
from ticketplace import assets
from ticketplace.models import db, Company, Content
from ticketplace.filters import register_filters

from ticketplace.extensions import (
    cache,
    assets_env,
    debug_toolbar,
    login_manager
)


def create_app(object_name, env="production"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. ticketplace.settings.ProductionConfig

        env: The name of the current environment, e.g. production or development
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize flask-bootstrap
    Bootstrap(app)

    # initialize SQLAlchemy
    db.init_app(app)

    # initialize flask-login
    login_manager.init_app(app)

    # initialize flask-admin
    admin = Admin(app, name='microblog', template_mode='bootstrap3')

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register our blueprints
    app.register_blueprint(eduticket, url_prefix='/tintranet')
    app.register_blueprint(main)

    # register admin views
    admin.add_view(CompanyView(Company, db.session))
    admin.add_view(ContentView(Content, db.session))

    # register filters
    register_filters(app)

    return app
