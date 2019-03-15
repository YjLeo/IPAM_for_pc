# coding=utf-8
import traceback

import redis
class Redis(object):
    def __init__(self,host,**redis_kwargs):
        self.pool = redis.ConnectionPool(host=host, port=6379,db=1)
        self.__db= redis.Redis(connection_pool=self.pool,**redis_kwargs)
    def clear_all(self):
        return self.__db.flushdb()

    def setValue(self,key, value):
            r = redis.Redis(connection_pool=self.pool)
            r.set(key, value)

    def getValue(self,key):
            r = redis.Redis(connection_pool=self.pool)
            return r.get(key)

    def incrValue(self,key):
            r = redis.Redis(connection_pool=self.pool)
            r.incr(key, 1)

    def decrValue(self,key):
            r = redis.Redis(connection_pool=self.pool)
            r.decr(key, 1)

    def delValue(self,key):
            r = redis.Redis(connection_pool=self.pool)
            r.delete(key)





class RedisQueue(object):
    def __init__(self, name,host,namespace='vlan128',**redis_kwargs):
       pool = redis.ConnectionPool(host=host, port=6379,db=0)
       # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
       self.__db= redis.Redis(connection_pool=pool,**redis_kwargs)
       self.key = '%s:%s' %(namespace, name)

    def clear_all(self):
        return self.__db.flushdb()
    def qsize(self):
        return self.__db.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        self.__db.rpush(self.key, item)  # 添加新元素到队列最右方

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__db.blpop(self.key, timeout=timeout)
        # if item:
        #     item = item[1]  # 返回值为一个tuple
        return item

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__db.lpop(self.key)
        return item
