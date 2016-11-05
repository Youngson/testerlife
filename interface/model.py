from flask_login import UserMixin
from . import db, bcrypt


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')


class User(db.Model):
    '''用户基础信息表'''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    nickname = db.Column(db.String(128))
    avatar = db.Column(db.String(128))
    user_auth = db.relationship('User_Auth', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.nickname


class User_Auth(db.Model, UserMixin):
    '''用户授权信息表'''
    __tablename__ = "user_auths"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    identity_type = db.Column(db.String(32))  # 登录类型（手机号[phone] 邮箱[email] 用户名[username]）或第三方应用名称（微信 微博等）
    identifier = db.Column(db.String(128))  # 标识（手机号 邮箱 用户名或第三方应用的唯一标识）
    credential = db.Column(db.String(128))  # 密码凭证（站内的保存密码，站外的不保存或保存token）

    @property
    def password(self):
        raise AttributeError('password不是可读属性')

    @password.setter
    def password(self, _password):
        if self.identity_type in ('phone', 'email', 'username'):
            self.credential = bcrypt.generate_password_hash(_password)
        else:
            self.credential = _password

    def verify_password(self, _password):
        if self.identity_type in ('phone', 'email', 'username'):
            return bcrypt.check_password_hash(self.credential, _password)
        else:
            return bool(self.credential == _password)

    def __repr__(self):
        return '<User_Auth %r>' % self.identifier
