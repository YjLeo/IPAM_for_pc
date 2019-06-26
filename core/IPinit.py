# coding=utf-8
import json
import os
from time import sleep
import sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


#import iptc

import requests
###清空cache
from requests.auth import HTTPBasicAuth

class foo:
    @staticmethod
    def get_ip(token):
        url = "http://192.168.128.201/api/apiclient/addresses/first_free/13/"
        payload = ""
        headers = {
            'token': token,
            'cache-control': "no-cache",
        }
        try:
            response = requests.request("POST", url, data=payload, headers=headers)
            ip = (response.json()['data'])
            print ip
        except Exception as e:
            return "None"
        print "get "+ip
        return ip
    @staticmethod
    def rec_ip(token,ips):
        if ips =='None':
            return ips
        url = "http://192.168.128.201/api/apiclient/addresses/" + ips + "/13/"
        payload = ""
        headers = {
            'token': token,
            'cache-control': "no-cache",
        }
        try:
            response = requests.request("DELETE", url, data=payload, headers=headers)
        except:
            return
        print( str(ips) + " dele from ipam")
        return str(ips)
    def token(self):
        url = "http://192.168.128.201/api/apiclient/user/"
        payload = ""
        headers = {}
        try:
            response = requests.request("POST", url, data=payload, headers=headers, auth=HTTPBasicAuth('leo', 'pconline'))
            token=(response.json()['data']['token'])
            return token
        except:
            print response.json(),"token error "+"token:"+token
            return


from core.Connect import redis
##清空需要回收的子网
def clear_all():
    redis.connect('').clear_all()
def len_allocat():
    len_all = redis.connect('allocated').qsize()
    return len_all
def len_unallocat():
    len_all = redis.connect('unallocated').qsize()
    return len_all
def get_allocated_ip():
    rev=redis.connect('allocated').get_nowait()
    return rev
def clean_redis():
    len_all,len_unall=1,1
    while len_all or len_unall !=0:
        clear_all()
        print "清除所有cache"
        sleep(20)
        len_all = redis.connect('allocated').qsize()
        len_unall = redis.connect('unallocated').qsize()
        print "Cache 可分配IP:"+str(len_all)
        print "Cache 可回收IP:"+str(len_unall)
        print "Cache清理完成"
def init_store():
    id_store = redis.connectmap()
    id_store.clear_all()


def search_DB():
    IPAM=foo()
    headers = {
        'token':IPAM.token() ,
        'cache-control': "no-cache",
    }
    rev = requests.request("GET", "http://192.168.128.201/api/apiclient/subnets/13/addresses/", headers=headers)
    dict=[]
    for i in rev.json()['data']:
        if i['tag'] == '2':
           dict.append(i['ip'].encode('utf-8'))
    return list(dict)
def search_k8s():
    rev=requests.request("GET","http://192.168.128.110:80/api/v1/pods")
    pods=rev.json()['items']
    ipdict=[]
    for i in pods:
        if i['status']['phase']!='Failed':
            try:
                if 'podIP' in i['status']:
                    ipdict.append(i['status']['podIP'].encode('utf-8'))
            except Exception as e:
                print e
                continue
    return list(ipdict)
def search_pod_health():
    rev = requests.request("GET", "http://192.168.128.110:80/api/v1/pods")
    pods = rev.json()['items']
    dict=[]
    for i in pods:
        if i['status']['phase'] != 'Failed':
            if 'running'not in i['status']['containerStatuses'][0]['state']:
                dict.append(i+'\t'+i['status']['containerStatuses'][0]['state'])
    if len(dict)>0:
        print "系统异常,请检查"
        raise list(dict)
                    ##warn
def Sync_idmap():
    print "清理旧ID映射表"
    redis.connectmap().clear_all()
    rev=requests.request("GET","http://192.168.128.110:80/api/v1/pods")
    pods=rev.json()['items']
    print "开始同步映射ID表"
    for i in pods:
        if i['status']['phase']!='Failed':
            try:
                if 'podIP' in i['status']:
                    #ipdict.(i['status']['containerStatuses'][0].encode('utf-8'))
                    redis.connectmap().setValue(i['status']['containerStatuses'][0]['containerID'].split('//')[1].encode('utf-8'),i['status']['podIP'].encode('utf-8'))
            except Exception as e:
                print e
                print "异常，请检查."
                continue
    print "完成同步映射ID表"











