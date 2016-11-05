#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-05 23:43
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-05 23:43

from flask import render_template,current_app
from flask_login import login_required,current_user
from . import api, admin

@admin.route('/')
def index():
    return render_template('index.html')