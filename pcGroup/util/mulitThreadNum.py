#!/usr/bin/python
#-*- coding: utf-8 -*-
#Edited By Sky 2017-07-17

'''
   用于封装多线程原子性操作
'''
import time
import encryptUtil
import redisUtil
import timeUtil



def getName():
    name = None
    try:
       name = encryptUtil.getUuid()
    except:
        name = timeUtil.getNowMillTime()
    try:
        redisUtil.setValue(str(name) , 0 , 3600)
    except:
        name = None
    return str(name)

def setTempValue(name , value , expire = 60):
    try:
        redisUtil.setValue(name , value , expire)
        True
    except:
        return  False

def getTempValue(name):
    try:
        return redisUtil.getValue(name)
    except:
        return None

def incrValue(name):
    try:
        redisUtil.incrValue(name)
        return True
    except:
        return False

def decrValue(name):
    try:
        redisUtil.decrValue(name)
        return True
    except:
        return False

def getNowValue(name):
    try:
        return  redisUtil.getValue(name)
    except:
        return None

def isFinish(name):
    result = False
    try:
        while(1>0):
            nowValue = getNowValue(name)
            if nowValue != None and int(nowValue) < 1:
                time.sleep(1)
                break
        return True
    except:
        return False

def isNewThread(name , threadNum):
    result = False
    try:
        nowValue = getNowValue(name)
        if nowValue != None and int(nowValue) < threadNum:
            return True
    except:
        return False