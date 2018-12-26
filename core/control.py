# coding=utf-8
from core import Connect
from core.Connect import redis

id_store = redis.connectmap()
unallocated = redis.connect('unallocated')
allocated = redis.connect('allocated')
class ip:

    #回收IP
    @staticmethod
    def rec_ip(ips):
        unallocated.put(ips)
        return ips
    #从redis队列拿IP
    @staticmethod
    def get_ip():
        ip=allocated.get_nowait()
        return ip

class Store:

    @staticmethod
    def put_dockerid(key,value):
        #{"dockerid","ip"} return ip
        id_store.setValue(key,value)
        return value
    @staticmethod
    def get_dockerip(key):
        #{"dockerid", "ip"} return ip
        return id_store.getValue(key)
    @staticmethod
    def del_dockerid(key):
        id_store.delValue(key)
        return key



