# coding=utf-8
from time import sleep
import sys
sys.path.append("..")
import iptc

import requests
###清空cache
from requests.auth import HTTPBasicAuth

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
    headers = {
        'token': 'HXIxUOljGo5LAX=.3r-_sFTA',
        'cache-control': "no-cache",
    }
    rev = requests.request("GET", "http://192.168.128.201/api/apiclient/subnets/11/addresses/", headers=headers)
    dict=[]
    for i in rev.json()['data']:
        if i['tag'] == '2':
           dict.append(i['ip'].encode('utf-8'))
    return list(dict)
def search_k8s():
    rev=requests.request("GET","http://192.168.128.110:80/api/v1/pods")
    pods=rev.json()['items']
    dict=[]
    for i in pods:
        if i['status']['phase']!='Failed':
            try:
                if 'podIP' in i['status']:
                    print i['status']['podIP']
                    dict.append(i['status']['podIP'].encode('utf-8'))
            except Exception as e:
                print e
                continue
    return list(dict)
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



if __name__ == '__main__':

    search_pod_health()
    print "K8S系统正常"
    if len_allocat()>=1500:
        #不初始化
         print "IP余量大于1500不进行初始化:"+str(len_allocat())
    else:
        ###封端口
        print '开始关闭端口'
        table = iptc.Table(iptc.Table.FILTER)
        chain = iptc.Chain(table, "INPUT")
        rule = iptc.Rule()
        match = iptc.Match(rule, 'tcp')
        rule.add_match(match)
        match.dport='5000'
        target = rule.create_target("DROP")
        print  '##清空队列所有cache'
        clean_redis()
        uselist = search_k8s()
        allip=search_DB()
        print "获取网段IP总量完成:"+str(len(allip))
        Unuse=[i for i in allip if i not in uselist]
        print "计算可用IP数:"+str(len(Unuse))
        print type(Unuse)
        for ip in Unuse:
            print ip
            redis.connect('allocated').put(ip)












    #get k8s ip list

