# coding=utf-8
import requests


def clear_cache():
    while 1:
        response=requests.request("GET","http://192.168.20.7:5000/api/v1/get_free_ip/")
        if not response.json():
            break
        else:
            if response.json()=='192.168.133.250':
                print "here"
            print response.json()


##清空需要回收的子网
def clear_cache_un():
    while 1:
        response=requests.request("GET","http://192.168.20.7:5001/api/v1/get_free_ip/")
        if not response.json():
            break
        else:
            print response.json()

