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


class Result(object):
    @staticmethod
    def success(message='Success', result=None, url=None):
        return {"message": message, "result": result, "error": False, "url": url}

    @staticmethod
    def error(message='Invalid', result=None, url=None):
        return {"message": message, "result": result, "error": True, "url": url}
