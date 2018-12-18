#!/usr/bin/python
#-*- coding: utf-8 -*-

import traceback ,  time , datetime


def timeFormat(timestamp):
    '''
        Format time , %Y-%m-%d %H:%M:%S
    '''
    try:
        if len(str(timestamp))== 10:
            timestring = time.localtime(float(str(timestamp)))
            result = time.strftime('%Y-%m-%d %H:%M:%S' , timestring)
        else:
            timestring = time.localtime(float(str(timestamp/1000)))
            result = time.strftime('%Y-%m-%d %H:%M:%S' , timestring)
        return result
    except:
        traceback.print_exc()
        return ""

def defaultimeRange():
    '''
        get now time  and half an hour ago  , base on timestamp
    '''
    try:
        nowtime = time.time()
        starttime = nowtime - 1800
        return starttime , nowtime
    except:
        traceback.print_exc()
        return ""

def defaultimeMRagne():
    '''
        get now time  one minute ago  , base on timestamp
    '''
    try:
        nowtime = time.time() - 60
        starttime = nowtime - 120
        return starttime , nowtime
    except:
        traceback.print_exc()
        return ""

def defaultTimeMillRagne(bet=1800):
    '''
      get now time  and half an hour ago  , base on timestamp ,millsecond
  '''
    try:
        nowtime = time.time()
        starttime = nowtime - bet
        return int(int(starttime) * 1000), int(int(nowtime) * 1000)
    except:
        traceback.print_exc()
        return ""
'''
获取上一分钟的范围
'''
def lastMinRange(intputTime = None):
    if intputTime == None:
        intputTime = time.time()
    lastMillTime = int(intputTime) - 60
    if len(str(lastMillTime))== 10:
        timestring = time.localtime(float(str(lastMillTime)))
        startTimeStr = time.strftime('%Y-%m-%d %H:%M:00' , timestring)
        endTimeStr = time.strftime('%Y-%m-%d %H:%M:59' , timestring)
        startTime = int(time.mktime(time.strptime(startTimeStr ,'%Y-%m-%d %H:%M:%S'))) * 1000
        endTime = int(time.mktime(time.strptime(endTimeStr , '%Y-%m-%d %H:%M:%S'))) * 1000
        return  startTime , endTime



def defaultimeUTCRange():
    '''
        get now time  and half hour ago  , base on timestamp to UTC
    '''
    try:
        nowtimestamp = int(time.time())
        nowtime = (nowtimestamp+28800)*1000000000
        starttime = (nowtimestamp -  1800+ 28800)*1000000000
        return starttime , nowtime
    except:
        traceback.print_exc()
        return ""

def defaultimeMSRagne():
    try:
        t = time.time()
        nowtime = int(round(t * 1000))
        starttime = nowtime - 1800000
        return starttime , nowtime
    except:
        traceback.print_exc()
        return ""

'''
获取前几天同一时间
@提取15分钟前的数据
@1 min = 60000 ms
'''
def month1timeMSRagne(num, t = None):
    try:
        day1ms = 86400000
        if t is None:
            t = time.time()
        nowtime = int(round(t * 1000 - 15*60000))
        lasttime = nowtime - num * day1ms
        starttime = lasttime - 60000
        return starttime, lasttime
    except:
        traceback.print_exc()
        return ""

'''
获取前n天日期时间
@num=0时为当天日期
'''
def getLastDay(num):

    try:
        today = datetime.date.today()
        nDay = datetime.timedelta(days=num)
        lastNDay = today-nDay
        return lastNDay
    except:
        traceback.print_exc()
        return None

'''
时间戳转时间
'''
def returnDate(timestamp):
    return datetime.date.fromtimestamp(timestamp)

#获取结束时间和开始时间之间的天数日期(YYYY-MM-DD)数组
'''
   @:param startTimestamp:开始时间戳
   @:param endTimestamp:结束时间戳
   @:return lists:YYYY-MM-DD
   mark:为了照顾cdn的日志隔天查询,返回时间后往后加一天
'''
def getBetweenDays(startTimestamp , endTimestamp):
    today = datetime.date.today()
    endTimeDate = returnDate(endTimestamp)
    startTimeDate = returnDate(startTimestamp)
    if startTimestamp > endTimestamp: return None
    nDay = datetime.timedelta(days=1)
    cdnDay = endTimeDate + nDay
    lastDay = endTimeDate
    betweenDays = []
    betweenDays.append(lastDay)
    while lastDay != startTimeDate:
        lastDay = lastDay - nDay
        betweenDays.append(lastDay)
    if lastDay != endTimeDate and lastDay != startTimeDate:
        betweenDays.append(lastDay)
    if today != endTimeDate:
        betweenDays.append(cdnDay)
    return  betweenDays

def getIndexBetweenDays(index , startTimestamp , endTimestamp):
    betweenDays = getBetweenDays(startTimestamp , endTimestamp)
    indexDays = ""
    for i in range(0 , len(betweenDays)):
        indexDays = indexDays + index + str(betweenDays[i])[4:] + ","
    return indexDays[0:len(indexDays)-1]

def getNowMillTime():
    return  int(time.time()) * 1000

'''
获取适合es天分索引格式的日期表达
'''
def getEsIndexSuffix():
    return str(time.strftime("-%m-%d"))