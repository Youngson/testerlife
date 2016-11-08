#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-05 23:43
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-05 23:43

from flask import render_template, current_app,flash,request,redirect,url_for
from flask_login import login_required, current_user
from . import admin
from .forms import UserForm,UserAuthForm
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

@admin.route('/user-edit/<int:uid>', methods=['GET', 'POST'])
@login_required
def user_edit(uid):
    uid = request.args.get('uid')
    user = User.query.get_or_404(uid) if uid is not None else User()
    user_auth = UserAuth.query.filter_by(user_id=uid).all() #if uid is not None else None
    form = UserForm(request.form,user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('用户添加成功')
        return redirect(url_for('.user_auth_edit',uid=user.id))
    return render_template('edit.html',form=form,rs=user_auth)


@admin.route('/user-del/<int:uid>')
def user_del(uid=0):
    user = User.query.get_or_404(uid)
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功')
    return redirect(url_for('admin.user'))


@admin.route('/user-auth-edit', methods=['GET', 'POST'])
def user_auth_edit():
    uid = request.args.get('uid')
    uaid = request.args.get('uaid')
    if uid:
        user_auth = UserAuth.query.filter_by(user_id=uid).all()
        _user_auth = UserAuth.query.get_or_404(uaid) if uaid is not None else UserAuth(user_id=uid)
        form = UserAuthForm(request.form,_user_auth)
        if form.validate_on_submit():
            if UserAuth.query.filter_by(identifier=form.identifier.data).first() is None:
                form.populate_obj(_user_auth)
                db.session.add(_user_auth)
                db.session.commit()
                flash('登录账号添加成功')
                return redirect(url_for('.user'))
            else:
                flash('此帐户名已被占使用')
        return render_template('edit.html',form=form,rs=user_auth)
    else:
        return redirect(url_for('.user_edit'))


@admin.route('/user-auth-del/<int:uaid>')
def user_auth_del(uaid=0):
    uid = request.args.get('uid')
    user_auth = UserAuth.query.get_or_404(uaid)
    db.session.delete(user_auth)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('admin.user_edit',uid=uid))