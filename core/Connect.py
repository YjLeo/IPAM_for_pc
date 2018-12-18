# coding=utf-8
import ConfigParser
import os
from Queueredis.RedisQueueUtil import RedisQueue, Redis


class redis:
    @staticmethod
    def connect(name):
        re_host= redis.read_config()
        return RedisQueue(name,re_host)
    @staticmethod
    def connectmap():
        re_host = redis.read_config()
        return Redis(re_host)
    @staticmethod
    def read_config():
        cp = ConfigParser.SafeConfigParser()
        mainConf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + "/conf/main.conf"
        cp.read(mainConf)
        re_host = cp.get("redis", "host")
        return re_host
class db(object):
    pass




