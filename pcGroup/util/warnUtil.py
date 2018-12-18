#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib,urllib2,json,time
def sendwarn(data):

    for i in data:
        data[i] = urllib.quote(data[i])
    data['ins_time'] = time.strftime("%Y-%m-%d_%H:%M:%S")
    #url='http://14.23.152.212/warn_info'  #公网
    url='http://192.168.10.87:80/put'   #内网
    json_data = json.dumps(data)
    print json_data
    req = urllib2.Request(url, json_data)
    response = urllib2.urlopen(req)
    return response.read()