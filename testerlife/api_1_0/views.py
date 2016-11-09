#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-07 23:01
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-07 23:01

import json
from flask import request, current_app,redirect,url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Api, Resource

from . import api
from .forms import UserForm,UserAuthForm
from .. import alembic,db
from ..model import User,UserAuth,Role
from ..util.result import Result

api = Api(api)


@api.resource('/alembic/<action>')
class DBAlembic(Resource):
    '''DBAlembic   数据库版本管理
    Youngson Create at 2016-11-08 15:13

    current():当前版本列表
    heads():获取没有子版本的版本列表
    log(start='base', end='heads'):按运行顺序获取版本列表
    branches():版本分支列表
    revision(message):创建新版本
    upgrade(target='heads'):升级
    downgrade(target=-1):降级
    merge(revisions='heads'):合并修订
    stamp(target='heads'):设置当前数据库版本
    '''
    def post(self, action=None):
        if action is not None:
            parm = '()' if action != 'revision' else '("made changes")'
            try:
                result = eval(''.join(['alembic.', action, parm]))
            except Exception as e:
                result = {"error":e}
        current_app.logger.info(result)

        return {"result": str(result)}

@api.resource('/init/<table>')
class DBInit(Resource):
    '''DBInit   初始化基础数据
    Youngson Create at 2016-11-09 11:13
    '''
    def __init__(self):
        '''Constructor for DBInit'''
        pass

    def get(self):
        pass

    def post(self,table):
        if table == 'role':
            result = Role.init_role()
        if table == 'user':
            result = User.init_user()
        if table == 'user_auth':
            result = UserAuth.init_user_auth()

        return {"result": result}

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def head(self):
        pass

    def options(self):
        pass


@api.resource('/auth')
class AuthLogin(Resource):
    '''AuthLogin   用户登录管理
    Youngson Create at 2016-11-07 19:13
    '''
    def post(self):
        '''用户登录'''
        user = UserAuth.query.filter_by(identifier=request.form.get('username')).first()
        if user is not None and user.verify_password(request.form.get('password')):
            login_user(user, False)
            url = '/admin/' if user.user.role.name == 'Admin' else '/index/'
            return Result.success(result="user_info", url=url)
        return Result.error('用户名不存在或者密码错误')

    @login_required
    def get(self):
        """注销登录"""
        logout_user()
        return Result.success()

@api.resource('/token')
class AuthToken(Resource):
    '''AuthToken
    Youngson Create at 2016-11-09 16:47
    '''
    def __init__(self):
        '''Constructor for AuthToken'''
        pass

    @login_required
    def get(self):
        token = current_user.generate_auth_token()
        return {'token': token.decode()}

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def head(self):
        pass

    def options(self):
        pass

@api.resource('/user')
class AdminUser(Resource):
    '''AdminUser    管理
    Youngson Create at 2016-11-08 23:13
    '''
    def __init__(self):
        """Constructor for AdminUser"""
        pass

    def get(self):
        pass

    @login_required
    def post(self):
        uid = request.args.get('uid')
        user = User.query.get(uid) if uid is not None else User()
        user_auth = UserAuth.query.filter_by(user_id=uid).all()  if uid is not None else None
        form = UserForm(csrf_enabled=False)#request.form, user
        csrf_token = form.hidden_tag()
        current_app.logger.info(form.hidden_tag())
        current_app.logger.info(request.form)
        current_app.logger.info(request.get_json())
        form.csrf_token = csrf_token
        if form.validate_on_submit():
            form.populate_obj(user)
            return Result.success(user.create(),{"uid":user.id})
        else:
            return Result.error(result=form.errors)

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def head(self):
        pass

    def options(self):
        pass

@api.resource('/user-auth')
class AdminUserAuth(Resource):
    '''AdminUserAuth    用户登录账号管理
    Youngson Create at 2016-11-09 16:15
    '''
    def __init__(self):
        '''Constructor for AdminUserAuth'''
        pass

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def head(self):
        pass

    def options(self):
        pass
