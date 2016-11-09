#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-07 21:58
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-07 21:58

from flask import Flask, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from . import config

db = SQLAlchemy()
alembic = Alembic()
bootstrap = Bootstrap()
login = LoginManager()
login.session_protection = "strong"
login.login_view = 'auth.index'
login.login_message = '请登入账号再进行下一步操作!'
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    alembic.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1000')
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # auth module blueprint
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')  # admin module blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)  # index module blueprint

    return app


    # from logging import Formatter, DEBUG
    # from logging.handlers import RotatingFileHandler
    #
    # """app.logger is project logging module
    # """
    #
    # handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=1)
    # handler.setFormatter(Formatter(
    #     '%(asctime)s %(levelname)s: %(message)s '
    #     '[in %(name)s:%(lineno)d]'
    # ))
    # handler.setLevel(DEBUG)
    # app.logger.addHandler(handler)


    # db.create_all()
