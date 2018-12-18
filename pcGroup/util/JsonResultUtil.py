#!/usr/bin/python
#-*- coding: utf-8 -*-
#Created By Sky
import re

def __sucessful__(data):
    return '{"code":200,"data":%s}' % (data)

def __fail__(data , code=500):
    return '{"code":%s,"data":%s}' % (code , data)


def jsontransfer(data):
    if isinstance(data, dict):
        return {jsontransfer(key):jsontransfer(value) for key,value in data.iteritems()}
    if isinstance(data, list):
        return [jsontransfer(num) for num in data]
    if isinstance(data, unicode):
        return data.encode('utf-8')
    else:
        return data


def dictvaluetran(front, func, trankey,_list=False):
    if isinstance(front[0], dict):
        tmpdict = {}
        for key, value in front[0].iteritems():
            if isinstance(value, (dict,list)):
                front[0]=value
                tmpdict[key] = dictvaluetran(front, func, trankey,_list)
                    # elif trankey == key:
            elif re.search(trankey, key):
                front[0]=value
                tmpdict[key] = dictvaluetran(front, func, trankey,_list)
            else:
                tmpdict[key] = value
        return tmpdict
    elif isinstance(front[0], list):
        tmplist = []
        for value in front[0]:
            if isinstance(value, (dict,list)):
                front[0]=value
                tmplist.append(dictvaluetran(front, func, trankey,_list))
            elif _list:
                front[0]=value
                tmplist.append(dictvaluetran(front, func, trankey,_list))
            else:
                tmplist.append(value)
        return tmplist
    elif isinstance(front[0], (unicode,long, int, float, str)):
            return func(*front)
    else:
        raise Exception

