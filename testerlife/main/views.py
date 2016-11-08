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

from flask import render_template,current_app,request,jsonify
from flask_login import login_required,fresh_login_required,current_user
from . import main


@main.route('/', methods=['GET', 'POST'])
@fresh_login_required
def index():
    return render_template('index.html')

