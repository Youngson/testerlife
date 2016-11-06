#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-06 2:51
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-06 2:51

from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SelectField,PasswordField,SubmitField,HiddenField,FieldList,FormField
from ..model import User,UserAuth,Role

class UserForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [(role.id, role.name)
                                for role in Role.query.order_by(Role.name).all()]

    nickname = StringField()
    avatar = StringField()
    role_id = SelectField('Role', coerce=int, default=5)
    submit = SubmitField('Submit')


class UserAuthForm(FlaskForm):
    user_id = HiddenField()
    identity_type = SelectField('登录类型',choices=[('phone','phone'), ('email','email'), ('username','username')],default='username')
    identifier = StringField()
    password = PasswordField()
    submit = SubmitField('Submit')

