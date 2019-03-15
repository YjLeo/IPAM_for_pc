#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis , traceback

pool = redis.ConnectionPool(host='192.168.128.201', port=6379)

def setValue(key , value , expire = 600):
    try:
        r = redis.Redis(connection_pool=pool)
        r.set(key , value , expire)
    except:
        traceback.print_exc()
        print "redis set Value error"

def getValue(key):
    try:
        r = redis.Redis(connection_pool=pool)
        return r.get(key)
    except:
        traceback.print_exc()
        return None

def incrValue(key):
    try:
        r = redis.Redis(connection_pool=pool)
        r.incr(key , 1)
    except:
        traceback.print_exc()
        print "redis incr Value error"

def decrValue(key):
    try:
        r = redis.Redis(connection_pool=pool)
        r.decr(key , 1)
    except:
        traceback.print_exc()
        print "redis incr Value error"

def delValue(key):
    try:
        r = redis.Redis(connection_pool=pool)
        r.delete(key)
    except:
        traceback.print_exc()
        print "redis del Value error"

if __name__ == "__main__":
    setValue("aa",0)
    print getValue("aa")
    incrValue("aa")
    print  getValue("aa")
    decrValue("aa")
    print  getValue("aa")
