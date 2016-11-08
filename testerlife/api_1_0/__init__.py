#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-07 21:58
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-07 21:58

from flask import Blueprint

api = Blueprint('api_1_0', __name__)

from . import views