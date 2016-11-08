#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-05 23:45
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-05 23:45

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
