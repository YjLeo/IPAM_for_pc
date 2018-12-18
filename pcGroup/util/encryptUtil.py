#!/usr/bin/python
#-*- coding: utf-8 -*-

import traceback ,  uuid
import hashlib

'''
获取md5加密串
'''
def hexStr(inputstr):
    try:
        md5 = hashlib.md5()
        md5.update(bytes(inputstr))
        return md5.hexdigest()
    except:
        traceback.print_exc()
        return None

'''
获取uuid字符串
'''
def getUuid():
    return uuid.uuid1()