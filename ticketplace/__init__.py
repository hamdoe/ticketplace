#! ../env/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Minjune Kim'
__email__ = 'june@ticketplace.net'
__version__ = '0.1'

import os

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader

from ticketplace.controllers.main import main
from ticketplace import assets
from ticketplace.models import db
from ticketplace.filters import register_filters


from ticketplace.extensions import (
    cache,
    assets_env,
    debug_toolbar,
    login_manager
)


def create_app(object_name=None):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: Name of the config object.
                     ex) ticketplace.settings.ProductionConfig
    """

    app = Flask(__name__)

    # Configuration loading:
    #
    # ^ (High Priority)
    # | Set directly via envrionment variables.
    # |     ex) SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # | Set in Config object selected by environment variable `CONFIG` or via `object_name` argument
    # |     ex) app.config.from_object(os.environ.get('CONFIG'))
    # | Set in default Config
    # |     ex) `HerokuConfig` inherits `Config`
    # | (Low Priority)

    configuration_object_name = object_name or os.environ.get('CONFIG', None)
    if not configuration_object_name:
        raise Exception('No Configuration selected!')
    app.config.from_object(configuration_object_name)
    print('%s: App configs set with %s.' % (__file__, configuration_object_name))

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    login_manager.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register our blueprints
    app.register_blueprint(main)

    # register filters
    register_filters(app)

    return app
