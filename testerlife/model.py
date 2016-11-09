#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-09 12:48
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-09 12:48

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired,BadSignature
from flask import current_app
from flask_login import UserMixin
from . import db, bcrypt,login


@login.user_loader
def load_user(user_id):
    try:
        user = UserAuth.query.get(int(user_id))
        return user
    except:
        return None


class User(db.Model):
    '''用户基础信息表'''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128))
    avatar = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    user_auth = db.relationship('UserAuth', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.nickname

    @staticmethod
    def init_user():
        admin_role_id = Role.query.with_entities(Role.id).filter_by(name='Admin').first() or 1
        user_list=[('Admin',admin_role_id[0])]
        for user in user_list:
            if User.query.filter_by(nickname=user[0]).first() is None:
                rs = User(nickname=user[0],role_id=user[1])
                db.session.add(rs)
        result = db.session.commit()
        return result

    def create(self):
        if User.query.filter_by(nickname=self.nickname).first() is None:
            db.session.add(self)
            db.session.commit()
            return '用户添加成功'
        else:
            return '此用户名已经使用'


class UserAuth(db.Model, UserMixin):
    '''用户授权信息表'''
    __tablename__ = "user_auths"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    identity_type = db.Column(db.String(32))  # 登录类型（手机号[phone] 邮箱[email] 用户名[username]）或第三方应用名称（微信 微博等）
    identifier = db.Column(db.String(128),unique=True)  # 标识（手机号 邮箱 用户名或第三方应用的唯一标识）
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
        user = User.verify_auth_token(_password)
        if user:
            return True
        if self.identity_type in ('phone', 'email', 'username'):
            return bcrypt.check_password_hash(self.credential, _password)
        else:
            return bool(self.credential == _password)

    @staticmethod
    def init_user_auth():
        admin_user_id = User.query.with_entities(User.id).filter_by(nickname='Admin').first() or 1
        user_auth_list=[(admin_user_id[0],'username','admin','admin')]
        for user_auth in user_auth_list:
            if UserAuth.query.filter_by(identifier=user_auth[1]).first() is None:
                rs = UserAuth(user_id=user_auth[0],identity_type=user_auth[1],identifier=user_auth[2],password=user_auth[3])
                db.session.add(rs)
        result = db.session.commit()
        return result

    def generate_auth_token(self, expiration = 600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = UserAuth.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User_Auth %r>' % self.identifier


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def init_role():
        role_list = [
            ('Admin',False,0),
            ('项目经理', False, 0),
            ('项目主管', False, 0),
            ('成员', False, 0),
            ('Guest', True, 0),
        ]
        for role in role_list:
            if Role.query.filter_by(name=role[0]).first() is None:
                rs = Role(name=role[0],default=role[1],permissions=role[2])
                db.session.add(rs)
        result = db.session.commit()
        return result