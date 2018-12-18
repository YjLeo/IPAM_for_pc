# coding=utf-8
import multiprocessing

import requests
import thread
from gevent import sleep
from requests.auth import HTTPBasicAuth
from core.Connect import redis



class foo:


    @staticmethod
    def get_ip(token):
        url = "http://192.168.128.201/api/apiclient/addresses/first_free/11/"
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
            print response.json(),"foo_getIP"+"token:"+token
            return "None"
        print "get "+ip
        return ip
    @staticmethod
    def rec_ip(token,ips):
        if ips =='None':
            return ips
        url = "http://192.168.128.201/api/apiclient/addresses/" + ips + "/11/"
        payload = ""
        headers = {
            'token': token,
            'cache-control': "no-cache",
        }
        try:
            response = requests.request("DELETE", url, data=payload, headers=headers)
            ip = response.json()['data']['ip']
        except:
            raise response.json()
        print( ip + " dele from ipam")
        return ip
    def token(self):
        url = "http://192.168.128.201/api/apiclient/user/"
        payload = ""
        headers = {}
        try:
            response = requests.request("POST", url, data=payload, headers=headers, auth=HTTPBasicAuth('leo', 'pconline'))
            token=(response.json()['data']['token'])
            return token
        except:
            print response.json(),"foo_recIP"+"token:"+token
            return

class task:


    def __init__(self):
        self.token=None
        thread.start_new(self.daemon_token, ())
        while self.token==None:
            print "Getting token"
            sleep(1)
        self.unallocated = redis.connect('unallocated')
        self.allocated=redis.connect('allocated')
        self.get_timesleep=0.002
        self.rec_timesleep=0.002


    def daemon_token(self):
        while 1:
            sleep(1)
            phpipam=foo()
            temp_token=phpipam.token()
            if temp_token:
                self.token=temp_token
                sleep(300)
                print "token update"
            else:
                print "retry get token"


    def get_ip(self):
        sleep(self.get_timesleep)
        token=self.token
        if token:
            try:
                ##从phpipam拿IP
                ip=foo.get_ip(token)
                if ip != "None":
                    try:
                        self.allocated.put(ip)
                        self.get_timesleep=0.002
                    except:
                        #异常回收到phpipam
                        foo.rec_ip(token,ip)
                        print "put " + ip + " to allocated_pool False"
                    print "put "+ip+" to allocated_pool Ok"
                else:
                    self.get_timesleep=10
                    print "No allocated IP"
            except Exception as e:
                print e

    def rec_ip(self):
        sleep(self.rec_timesleep)
        token=self.token
        if token :
            unallocated = redis.connect('unallocated')
            ip=unallocated.get_nowait()
            if ip :
                try:
                    #从不可用列表拿出IP回收到IPAM
                    self.rec_timesleep = 0.002
                    print foo.rec_ip(token,ip)
                except Exception as e:
                    #异常  丢回可用列表cache
                    self.allocated.put(ip)
                    print str(ip)+" rec false return cache"
            else:
                self.rec_timesleep=10
                print "No unallocated IP"

    def get_ip_work(self):
            while 1:
                self.get_ip()

    def rec_ip_work(self):
            while 1:
                self.rec_ip()

def get_ip():
    a=task()
    a.get_ip_work()

def rec_ip():
    b=task()
    b.rec_ip_work()

def daemon():
    c=multiprocessing.Process(target=get_ip,args=())
    d=multiprocessing.Process(target=rec_ip, args=())
    c.start()
    d.start()


if __name__ == '__main__':
    daemon()




