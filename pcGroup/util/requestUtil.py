#!/usr/bin/python
#-*- coding: utf-8 -*-

import StringIO
import base64
import json
import pickle
import requests
import traceback
import urllib2
from tempfile import TemporaryFile
from pcGroup.log.logUtil import logUtil



logutil = logUtil()

def get(url , myHeaders = {'User-Agent':'PcGroup Util Client'}):
    result = None
    try:
        req = urllib2.Request(url,headers=myHeaders)
        f = urllib2.urlopen(req)
        result = f.read()
        f.close()
    except:
        result =  '{"status":"500","msgs":"Get URL Error"}'
        traceback.print_exc()
        logutil.errmsgStringIO(traceback , 'get URL error')
    return result

def post(url , data , myHeaders = {'User-Agent':'PcGroup Util Client','content-type': 'application/json; charset=UTF-8'}):
    result = None
    try:
        #print url
        #print data
        #print headers
        print data
        print url
        req = urllib2.Request(url, data, myHeaders , 30000)
        f = urllib2.urlopen(req)
        result = f.read()
        f.close()
    except:
        result =  '{"status":"500","msgs":"Post URL Error"}'
        logutil.errmsgStringIO(traceback , 'Post URL error')
        traceback.print_exc()
    return result

def fpost(myHeaders = {'User-Agent':'PcGroup Util Client' ,'content-type': 'application/json; charset=UTF-8' ,'Accept-Encoding': '*/*' }):
    url = 'http://192.168.12.81:9200/_bulk'
    data = "{ \"index\" : { \"_index\" : \"test2\", \"_type\" : \"log\"} }\n"
    data = data + "{\"ok\":\"a\"," + "\"ok2\":1}\n"
    data = data + "{\"ok\":\"b\"," + "\"ok2\":2}";
    temp = TemporaryFile()

    temp.writelines('{"index" : { "_index" : "test2", "_type" : "log"}}')
    temp.writelines('{"ok":"a","ok2":1}')
    #temp.write('{"ok":"a","ok2":1}')
    #temp.write(data)

    #temp.flush()
    temp.seek(0)
    print  temp.readline()
    print  temp.readline()
    print  temp.mode

    files = {'file': open('/Users/sky/Documents/company/esManager/pcPython/logs/test.log' , "rb")}

    #files = {'file': temp}


    r = requests.post( url , base64.b64encode(data.encode("utf8")).decode("ascii") , headers = myHeaders )

    print r.request.headers
    print r.headers

    #r = requests.request("POST" , url , files = files, headers = myHeaders)

    print r.text

def delete(url, myHeaders = {'User-Agent':'PcGroup Util Client'}):
    result = None
    try:
        print url
        req = requests.delete(url, headers=myHeaders)
        result =req.status_code
    except:
        result = '{"status":"500","msgs":"Delete URL Error"}'
        logutil.errmsgStringIO(traceback, 'Delete URL error')
        traceback.print_exc()
    return result

if __name__== "__main__":
    fpost()
