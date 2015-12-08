#! ../env/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Minjune Kim'
__email__ = 'june@ticketplace.net'
__version__ = '0.1'

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader

from ticketplace.controllers.main import main
from ticketplace import assets
from ticketplace.models import db

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

    # register fileters (refactor out into other file)
    from ticketplace.utils import kst_now

    @app.template_filter('number')
    def number_filter(n):
        """ 템플릿 용 숫자 필터. 버림하고 콤마 넣어줌 """
        return '{:,}'.format(int(n))

    @app.template_filter('age')
    def age_filter(interval):
        age_min, age_max = interval
        return '%d세 ' % age_min + ('~ %d세' % age_max if age_max < 99 else '이상')

    @app.template_filter('datetime')
    def datetime_filter(date, format='%Y/%m/%d(%a) %p %I:%M'):
        """
            템플릿 용 날짜 필터.
        """
        if not date:
            return '없음'
    
        # windows상의 strftime함수가 유니코드를 못읽어서 날짜를 파싱하고 다시 입력하는 뻘짓을 해야함
        result = format
        tokens = ('%a', '%A', '%b', '%B', '%c', '%d', '%H', '%I', '%j', '%m', '%M',
                  '%p', '%S', '%U', '%w', '%W', '%x', '%X', '%y', '%Y', '%Z', '%%')
        replacements = {token: date.strftime(token) for token in tokens}
        for token, variable in replacements.items():
            result = result.replace(token, variable)
    
        return result
    
    @app.template_filter('before')
    def timeago_filter(from_date, to_date=kst_now()):
        interval = to_date - from_date
        interval_second = int(interval.total_seconds())
        if interval_second < 60:
            return str(interval_second) + '초 전'
        elif interval_second < 60 * 60:
            return str(interval_second // 60) + '분 전'
        elif interval_second < 60 * 60 * 24:
            return str(interval_second // (60 * 60)) + '시간 전'
        elif interval_second < 60 * 60 * 24 * 30:
            return str(interval_second // (60 * 60 * 24)) + '일 전'
        elif interval_second < 60 * 60 * 24 * 365:
            return str(interval_second // (60 * 60 * 24 * 30)) + '개월 전'
        else:
            return str(interval_second // (60 * 60 * 24 * 365)) + '년 전'

    @app.template_filter('truncate')
    def truncate_filter(s, length, end='...'):
        """Return a truncated copy of the string."""
        if len(s) <= length:
            return s
        else:
            return s[:length] + end

    return app
