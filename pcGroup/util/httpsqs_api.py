#!/usr/bin/python
#coding:utf-8

'''
a = HttpsqsClient('192.168.1.1','1218','pass')
print a.put('logtest','sdfsfsf')
print a.get('logtest')
'''

import urllib,urllib2,json

class HttpsqsClient(object):
    def __init__(self,host= '192.168.234.21',port='1218',auth = '', charset = 'utf-8'):
        self.httpsqs_url = 'http://' + host + ':' + port + '/httpsqs?'
        self.httpsqs_auth = auth
        self.httpsqs_charset = charset

    def __http_get(self,params):
        '''
        http get??
        params = {"wd":"a","b":"2"}
        '''
        params['auth'] = self.httpsqs_auth
        params['charset'] = self.httpsqs_charset
        try:
            url_params = urllib.urlencode(params)
            final_url = self.httpsqs_url + url_params
            page = urllib2.urlopen(final_url,timeout=3).read()
            return page
        except urllib2.HTTPError, e:
            print "Error Code:", e.code
        except urllib2.URLError, e:
            print "Error Reason:", e.reason

    def __http_post(self,params,post_data):
        """
        http post??
        @param params: params = {"wd":"a","b":"2"}
        @param post_data: json or string
        @type post_data: string
        @return:string
        """
        params['auth'] = self.httpsqs_auth
        params['charset'] = self.httpsqs_charset

        url_params = urllib.urlencode(params)
        final_url = self.httpsqs_url + url_params
        post_data = str(post_data).encode('utf8')
        try:
            req = urllib2.Request(final_url, post_data)
            page = urllib2.urlopen(req,timeout=3).read()
            return page
        except urllib2.HTTPError, e:
            print "Error Code:", e.code
        except urllib2.URLError, e:
            print "Error Reason:", e.reason


    def put(self,queue_name,queue_data):
        params = {'opt':'put','name':queue_name}
        r = self.__http_post(params,queue_data)
        if r == 'HTTPSQS_PUT_OK':
            return True
        return False


    def get(self,queue_name):
        params = {'opt':'get','name':queue_name}
        r = self.__http_get(params)
        if r == 'HTTPSQS_GET_END':
            return None
        return r

    def status(self,queue_name):
        params = {'opt':'status','name':queue_name}
        return self.__http_get(params)

    def status_json(self,queue_name):
        params = {'opt':'status_json','name':queue_name}
        return self.__http_get(params)

    def reset(self,queue_name):
        params = {'opt':'reset','name':queue_name}
        return self.__http_get(params)

    def maxqueue(self,queue_name,num):
        params = {'opt':'maxqueue','name':queue_name,'num':str(num)}
        return self.__http_get(params)

    def synctime(self,queue_name,num):
        params = {'opt':'synctime','name':queue_name,'num':str(num)}
        return self.__http_get(params)