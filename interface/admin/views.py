#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-05 23:43
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-05 23:43

from flask import render_template, current_app,flash,request,redirect,url_for
from flask_login import login_required, current_user
from . import api, admin
from .forms import EditUserForm,UserForm,UserAuthForm
from .. import db
from ..model import User,UserAuth


@admin.route('/')
@login_required
def index():
    return render_template('index.html')


@admin.route('/user')
@login_required
def user():
    user = User.query.all()
    return render_template('user.html', rs=user)

@admin.route('/user-add', methods=['GET', 'POST'])
@login_required
def user_add():
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        current_app.logger.info(user)
        db.session.add(user)
        db.session.commit()
        flash('用户添加成功')
        return redirect(url_for('.user_auth_add',id=user.id))
    return render_template('edit.html',form=form)

@admin.route('/user-auth-add', methods=['GET', 'POST'])
def user_auth_add():
    id = request.args.get('id')
    if id:
        user = User.query.get_or_404(id)
        form = UserAuthForm(user_id=user.id)
        if form.validate_on_submit():
            current_app.logger.info(form.data)
            user_auth = UserAuth.query.filter_by(identifier=form.identifier.data).first()
            current_app.logger.info(user_auth)
            if user_auth is None:
                user_auth = UserAuth()
                form.populate_obj(user_auth)
                db.session.add(user_auth)
                flash('登录账号添加成功')
                return redirect(url_for('.user'))
            else:
                flash('此帐户名已被占使用')
        return render_template('edit.html',form=form)
    else:
        return redirect(url_for('.user_add'))


@admin.route('/user-del/<int:id>')
def user_del(id=0):
    pass