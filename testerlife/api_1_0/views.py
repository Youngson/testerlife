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
from ..model import User,UserAuth
from ..util.result import Result

api = Api(api)


@api.resource('/auth')
class AuthLogin(Resource):
    '''用户登录管理'''

    def post(self):
        """用户登录"""
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


@api.resource('/alembic/<action>')
class DBAlembic(Resource):
    '''数据库版本管理
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

    def get(self, action=None):
        if action is not None:
            parm = '()' if action != 'revision' else '("made changes")'
            result = eval(''.join(['alembic.', action, parm]))
        current_app.logger.info(result)

        return {"result": str(result)}


@api.resource('/user')
class AdminUser(Resource):
    """AdminUser管理
    """

    def __init__(self):
        """Constructor for AdminUser"""
        pass

    def get(self):
        pass

    # @login_required
    def post(self):
        uid = request.args.get('uid')
        user = User.query.get(uid) if uid is not None else User()
        user_auth = UserAuth.query.filter_by(user_id=uid).all()  # if uid is not None else None
        form = UserForm(request.form, user)
        current_app.logger.info(request.form)
        current_app.logger.info(request.get_json())
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            result = Result.success('用户添加成功')
            return result,201,redirect(url_for('.user_auth_edit', uid=user.id))
        else:
            current_app.logger.info(form.errors)
            return Result.error(result=form.errors)
        # return render_template('edit.html', form=form, rs=user_auth)

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass
