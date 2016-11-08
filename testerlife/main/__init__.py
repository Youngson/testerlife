#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Youngson
# @Eamil:  Youngson.Gu@gmail.com
# @Date:   2016-11-05 23:43
# @Last Modified by:   Youngson
# @Last Modified time: 2016-11-05 23:43

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
