#!/usr/bin/python
#-*- coding: utf-8 -*-
#Edited By Sky 2017-07-19

import os , thread , StringIO
import logging.config
import ConfigParser
import traceback

class logUtil():
    def __init__(self):
        cp = ConfigParser.SafeConfigParser()
        mainConf = os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")) + "/conf/main.conf"
        #print  mainConf
        cp.read(mainConf)
        loggerFile = cp.get("logger" , "loggerPath")
        logging.config.fileConfig(loggerFile)
        self.loggerinfo = logging.getLogger("loginfo")
        self.loggerwarn = logging.getLogger("logwarn")

    def errmsgformat(self, warninfo):
        for file, lineno, function, text in traceback.extract_tb(warninfo[2]):
            self.loggerwarn.warn(file + " line: " + str( lineno ) + " in " + function)
            self.loggerwarn.warn(text)

    def errmsgStringIO(self, warninfo  , msg):
        fp = StringIO.StringIO()
        warninfo.print_exc(file=fp)
        message = fp.getvalue()
        self.loggerwarn.warn(msg + '---' + message)

    def warnMsg(self , msg):
        self.loggerwarn.warn(msg)

    def infoMsg(self , msg):
        self.loggerinfo.info(msg)

if __name__ == "__main__":
    logutil = logUtil()