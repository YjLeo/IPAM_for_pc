# coding=utf-8
from time import sleep

import requests
###清空cache
from core.Connect import redis


def clear_cache():
    while 1:
        response=requests.request("GET","http://192.168.20.7:5000/api/v1/get_free_ip/")
        if not response.json():
            break
        else:
            print response.json()


##清空需要回收的子网
def clear_cache_un():
    while 1:
        response=requests.request("GET","http://192.168.20.7:5000/api/v1/get_free_ip/")
        if not response.json():
            break
        else:
            print response.json()
def clear_all():
    redis.connect('').clear_all()

def check_redis():
    len_all,len_unall=1,1
    while len_all or len_unall !=0:
        clear_all()
        print "清除所有cache"
        sleep(20)
        len_all = redis.connect('allocated').qsize()
        len_unall = redis.connect('unallocated').qsize()
        print "Cache 可分配IP:"+str(len_all)
        print "Cache 可回收IP:"+str(len_unall)

if __name__ == '__main__':
    check_redis()





    #get k8s ip list

