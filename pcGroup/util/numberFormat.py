#!/usr/bin/python
#-*- coding: utf-8 -*-
#Edited By Sky 2017-07-27

'''
   用于封装生成格式化数字,GB,M,TB
'''

'''
type : TB , GB , MB , auto
strShow : 是否显示单位
'''
def bytesFormat(bytesValue , type =  "auto" , strShow = False):
    result = None
    if type == "GB":
        result = ('%.2f' % float(float(bytesValue) / 1024 /1024 / 1024 ))
    elif type == "TB":
        result = ('%.1f' % float(float(bytesValue) / 1024 /1024 / 1024 / 1024 ))
    elif type == "MB":
        result = ('%.2f' % float(float(bytesValue) / 1024 /1024 ))
    elif type == "KB":
        result = ('%.1f' % float(float(bytesValue) / 1024 ))
    elif type == "B" :
        result = ('%.1f' % float(bytesValue))
    elif type == "auto":
        if float(bytesValue) > 1099511627776:
            result = ('%.1f' % float(float(bytesValue) / 1024 /1024 / 1024 / 1024 ))
            type = "TB"
        elif float(bytesValue) > 1073741824:
            result = ('%.1f' % float(float(bytesValue) / 1024 /1024 / 1024 ))
            type = "GB"
        elif float(bytesValue) > 1048576:
            result = ('%.1f' % float(float(bytesValue) / 1024 /1024 ))
            type = "MB"
        elif float(bytesValue) > 1024:
            result = ('%.1f' % float(float(bytesValue) / 1024 ))
            type = "KB"
        else:
            result = bytesValue
            type = "B"
    else:
        result = bytesValue
    if strShow == False:
        return  result
    else:
        return str(result) + type

def kilobytesFormat(bytesValue , type =  "auto" , strShow = False):
    result = None
    if type == "GB":
        result = ('%.1f' % float(float(bytesValue) / 1024 /1024  ))
    elif type == "TB":
        result = ('%.1f' % float(float(bytesValue) / 1024 /1024 / 1024  ))
    elif type == "MB":
        result = ('%.1f' % float(float(bytesValue) / 1024  ))
    elif type == "KB":
        result = ('%.1f' % float(float(bytesValue)  ))
    elif type == "auto":
        if float(bytesValue) > 1073741824:
            result = ('%.1f' % float(float(bytesValue) / 1024 /1024 / 1024  ))
            type = "TB"
        elif float(bytesValue) > 1048576:
            result = ('%.1f' % float(float(bytesValue) / 1024 / 1024 ))
            type = "GB"
        elif float(bytesValue) > 1024:
            result = ('%.1f' % float(float(bytesValue) / 1024 ))
            type = "MB"
        else:
            result = bytesValue
    else:
        result = bytesValue
    if strShow == False:
        return  result
    else:
        return str(result) + type

def numberPer(number ,reverse=True, strShow = False):
    result = ('%.3f' % float(100 - number * 100 )) if reverse else ('%.3f' % float(number))
    if strShow == True:
        return result + "%"
    else:
        return result

def divisonforPer(fractions,numerator,reverse=False):
    result=float(fractions)/numerator
    result=numberPer(result,reverse)
    return result

def timeInterval(startTimestamp,endTimestamp):
    timerange = endTimestamp - startTimestamp
    if timerange <= 900 :
        interval = 1 * 30
    if timerange <= 3600 and timerange > 900:
        interval = 1 * 60
    elif timerange > 3600 and timerange <= 10800:
        interval = 3 * 60
    elif timerange > 10800 and timerange <= 43200:
        interval = 10 * 60
    elif timerange > 43200 and timerange <= 86400:
        interval = 30 * 60
    elif timerange > 86400:
        interval = 1440 * 60
    return interval

'''
千分位格式化
type : int float
'''
def numberQian(number):
    return  '{:,}'.format(number)

if __name__ == "__main__":
    print  numberQian(11222341341.01098)