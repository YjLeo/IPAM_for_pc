#!/usr/bin/python
#-*- coding: utf-8 -*-
#Edited By Sky 2017-03-29

import ConfigParser
import StringIO
import os
import random
import sys
import traceback
import urllib2
import pcGroup.util.encryptUtil as  encryptUtil
import  pcGroup.util.redisUtil as redisUtil
from pcGroup.log.logUtil import logUtil






class searchUtil():
    def __init__(self):
        cp = ConfigParser.SafeConfigParser()
        mainConf = os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")) + "/conf/main.conf"
        cp.read(mainConf)
        esServers = cp.get("ES" , "servers").split(",")
        #print  esServers
        #self.servers = ["192.168.12.81"]
        self.servers = esServers
        self.headers = {'User-Agent':'PcGroup Util Client' , "Content-Type" : "application/json; charset=UTF-8"}
        self.logutil = logUtil()


    def get(self , url):
        result = None
        try:
            req = urllib2.Request(url,headers=self.headers)
            f = urllib2.urlopen(req)
            result = f.read()
            f.close()
        except:
            result =  '{"status":"500","msgs":"Get Elaticsearch Error"}'
            traceback.print_exc()
            self.logutil.errmsgStringIO(traceback , 'get URL error')
        return result

    def post(self , url , data):
        result = None
        try:
            #print url
            #print data
            #print headers
            # print data
            # print url
            req = urllib2.Request(url, data, self.headers, 30000)
            f = urllib2.urlopen(req)
            result = f.read()
            f.close()
        except:
            result =  '{"status":"500","msgs":"Post Elaticsearch Error"}'
            self.logutil.errmsgStringIO(traceback , 'get URL error')
            traceback.print_exc()
        return result

    '''
       @:param index:索引名字
       @:param type:索引类型
       @:param postData:查询条件
       @:param multiSearch:是否进行多条件查询
       @:param cache:是否启动redis缓存结果
       @:param key:redis缓存启用搭配使用,None系统自定义key,系统自定义组成为md5(index + type + postData)
       @:param accurate:是否进行索引进行查找,默认是模糊索引
    '''
    def searchELT(self , index , type , postData="", multiSearch=False, cache=False , key=None , accurate=None , serverINPUT = None):
        serverNum = random.randint(1 , len(self.servers)) - 1
        print  postData
        server = self.servers[serverNum]
        result = ""

        if serverINPUT != None:
            server = serverINPUT

        if cache == True:
            if key == None:
                key = encryptUtil.hexStr(index + type + postData)
            if key == None:
                result = None
            else:
                #print  "Key is : " , key
                result = redisUtil.getValue(key)
                print "Get Redis result : " , result
        if result != None and result != "":
            #print "Get Result from Redis : " , result
            return result

        indextype = ""
        if type == "normal":
            indextype =  "-extra"

        url = "http://%s/%s*%s/%s/_search" % (server , index , indextype , type)

        if accurate != None:
            url = "http://%s/%s/%s/_search" % (server , index  , type)

        if index == "all-ivy":
            url = "http://%s/%s*/%s/_search" % (server , index , type)

        if "chkurl-" in index or "netinfo_" in index:
            if multiSearch == True:
                url = "http://%s/%s/%s/_msearch" % (server , index  + indextype , type)
            else:
                url = "http://%s/%s/%s/_search" % (server , index  + indextype , type)
        print url
        result = ""
        if postData == "":
            result = self.get(url)
        else:
            result = self.post(url,postData)
        '''
            如果并发要求变高,则要进行redis存储异步.
        '''
        if cache == True:
            if key != None:
                if str(result).find("Post Elaticsearch Error") < 0:
                    redisUtil.setValue(key, result)
        return result

if __name__ == "__main__":
    sr = searchUtil()
    #print sr.searchELT("xueche","access",'{"query": { "match_all": {} },"from": 0,"size": 100}}')
    #print sr.searchELT("xueche","access",'{"query":{"bool":{"must":[{"range":{"createAt":{"gt":"2017-03-29 16:31:49"}}}]}}}')
    print sr.searchELT("netinfo_daily","log",'{"query": { "match_all": {} },"from": 0,"size": 100}}')