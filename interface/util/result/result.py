#!/usr/bin/env python
# -- coding: utf-8 --
'''
File Name : util.result.result
Description :
Author : Raymond
change Activity :
create file : C:/Users/Raymond/git/testerlife/util/result/result.py
create time :2016年11月3日
'''

class result:
    
    @staticmethod
    def success(url=None):
        return {'errMsg':None, 'result':'success', 'url':url}
    
    @staticmethod
    def error(url=None):
        return {'errMsg':"Login Error", 'result':'invalid', 'url':url}
