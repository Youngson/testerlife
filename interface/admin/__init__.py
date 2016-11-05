#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-05 23:42
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-05 23:42

from flask import Blueprint
from flask_restful import Api

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='assets')
api = Api(admin)

from . import views
