#!/usr/bin/python
#-*- coding: utf-8 -*-
#Edited By Sky 2017-07-17

import os
import traceback
import urllib2
import ConfigParser
from pcPython.pcGroup.log.logUtil import logUtil

class healthUtil():
    def __init__(self):
        cp = ConfigParser.SafeConfigParser()
        mainConf = os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")) + "/conf/main.conf"
        cp.read(mainConf)
        #loggerFile = cp.get("logger" , "loggerPath")
        #logging.config.fileConfig(loggerFile)
        #self.loggerinfo = logging.getLogger("loginfo")
        #self.loggerwarn = logging.getLogger("logwarn")
        self.headers = {'User-Agent':'PcGroup Util Client'}
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

    def healthGet(self , url , clusterIP):
        result = None
        try:
            result = self.get("http://" + clusterIP + url)
        except:
            result =  '{"status":"500","msgs":"Get Elaticsearch Error"}'
            traceback.print_exc()
            self.logutil.errmsgStringIO(traceback , 'get URL error')
        return result