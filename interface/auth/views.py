#!/usr/bin/env python
# -- coding: utf-8 --
'''
File Name : interface.auth.views
Description :
Author : Raymond
change Activity :
create file : C:/Users/Raymond/git/testerlife/interface/auth/views.py
create time :2016年11月1日
'''

from flask import render_template, request, jsonify,current_app
from flask_restful import Resource
from flask_login import login_user, logout_user, login_required
from interface.util.result.result import result
from . import api, auth
from .. import login
from ..model import User,UserAuth


@login.user_loader
def load_user(user_id):
    try:
        user = UserAuth.query.get(int(user_id))
        return user
    except:
        return None


@auth.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')


@api.resource('/login')
class login(Resource):
    def post(self):
        args = request.form
        user = UserAuth.query.filter_by(identifier=args.get('username')).first()
        if user is not None and user.verify_password(args.get('password')):
            login_user(user)
            url = '/admin/' if user.user.role.name=='Admin' else '/index/'
            return jsonify(result.success(url))
        return jsonify(result.error())


@api.resource('/logout')
class logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return jsonify(result.success())
