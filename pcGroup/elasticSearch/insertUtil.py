#!/usr/bin/python
#-*- coding: utf-8 -*-
#Edited By Sky 2017-07-24


import pcPython.pcGroup.util.requestUtil as  requestUtil
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class insertUtil():
    '''
        esServer : elasticsearch的服务端口,eg:192.168.12.81:9200
        index:索引名字
        type:类型
        data:json字符串数据
    '''
    def insertSingle(self , esServer , index , type , data , headers = None):
        url = "http://%s/%s/%s" % (esServer , index , type)
        if headers == None:
            headers = {'User-Agent':'PcGroup Util Client',"Content-Type" : "application/json; charset=UTF-8"}
            requestUtil.post( url , data , headers)
        else:
            requestUtil.post( url , data , headers )

    '''
        esServer : elasticsearch的服务端口,eg:192.168.12.81:9200
        index:索引名字
        type:类型
        data:列表中包含字典:[{"ok":1,"ok2":2,"ok3":"ok3"}]
            data = []
            dataDict = {"ok":1,"ok2":2,"ok3":"ok3"}
            data.append(dataDict)
            data.append(dataDict)
    '''
    def insertBluk(self , esServer , index , type  , data):
        es = Elasticsearch( esServer )
        if isinstance(data,dict):
            actions = [{'_op_type': 'index', '_index': index, '_type': type, '_source': d} for d in data.itervalues()]
        else:
            actions = [{'_op_type': 'index','_index' : index ,'_type' : type , '_source':d} for d in data]
        bulk(es , actions)


    def setMapping(self,esServer, index_name, doc_type="logs", field_type=(("esDate","date"),)):
        es = Elasticsearch(esServer)
        if not es.indices.exists(index=index_name):
            innerdict={field[0]:{"type":field[1],
                                 } for field in field_type}

            my_mapping = {
                "%s"%(doc_type): {
                    "properties":
                        innerdict

                }
            }

            create_index = es.indices.create(index=index_name)
            mapping_index = es.indices.put_mapping(index=index_name, doc_type=doc_type,
                                                   body=my_mapping)




if __name__== "__main__":
    # inserutil = insertUtil()
    data = []
    dataDict = {"ok":1,"ok2":2,"ok3":"ok3"}
    data.append(dataDict)
    data.append(dataDict)
    # inserutil.insertBluk("192.168.12.81:9200" , "test5" , "logs" , data)
    inserutil = insertUtil()
    inserutil.setMapping("192.168.12.81:9200","testmap",field_type=(("ip","keyword"),("time","date"),("name","text")))
    inserutil.insertBluk("192.168.12.81:9200", "testmap", "logs", data)