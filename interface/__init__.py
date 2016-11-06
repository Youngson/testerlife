from flask import Flask, redirect
from flask_restful import Api
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from logging import Formatter, DEBUG
from logging.handlers import RotatingFileHandler
from . import config

app = Flask(__name__)
app.config.from_object(config)
api = Api(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.session_protection = "strong"
login.login_view = 'auth.index'
login.login_message = '请登入账号再进行下一步操作!'
bcrypt = Bcrypt(app)
"""app.logger is project logging module
"""

handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(name)s:%(lineno)d]'
))
handler.setLevel(DEBUG)
app.logger.addHandler(handler)

from .auth import auth

app.register_blueprint(auth, url_prefix='/auth')  # auth module blueprint
from .admin import admin

app.register_blueprint(admin, url_prefix='/admin')  # admin module blueprint
from .index import index

app.register_blueprint(index, url_prefix='/index')  # index module blueprint
app.add_url_rule('/', None, lambda x='/index': redirect(x))
# db.create_all()