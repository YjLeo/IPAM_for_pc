#!/usr/bin/python
#-*- coding: utf-8 -*-
import traceback , json , urllib2

'''
   condition的type只支持四种类型
        [{"type":"","key":"字段名字","value":"字段的值"}]
         type:
              s=:字符串等于 
              sp:字符串匹配
              number:数字类型， min=<x<=max
              prefix:以什么开头
    添加多一个or添加支持
    {"type":"","key":"字段名字","value":"字段的值","mtype":""}
    type: many
    mtype: s= | number
'''
def assembleQR(reqM):
    result = ""
    tiaojian = []
    try:
        reqMjson = json.loads(reqM, encoding="utf-8")
        for i in range(0 , len(reqMjson)):
            type = reqMjson[i]["type"]
            key = reqMjson[i]["key"]
            value = reqMjson[i]["value"]
            if type == "number":
                lte = value.find("x<=")
                gte = value.find("=<x")
                tmpvalue = ""
                if gte > -1:
                    gteval = value[0:gte]
                    tmpvalue = tmpvalue + '"gte":' + gteval + ","
                if lte > -1:
                    lteval = value[lte+3:len(value)]
                    tmpvalue = tmpvalue + '"lte":' + lteval + ","
                rangeval = '{"range":{"' + key  + '":{' + tmpvalue[0:len(tmpvalue)-1] + '}}}'
                tiaojian.append(rangeval)
            elif type == "s=":
                keytmp = key + ".keyword"
                if key == "st" or key == "localDnsResponseCode" or key == "id":
                    keytmp = key
                stringmatch = '{"term":{"' + keytmp + '":"' + value + '"}}'
                tiaojian.append(stringmatch)
            elif type == "sp":
                if key == "url" or key == "uri" or key.find("Appsession") > 0 or key == "URL" or key == "WANGSUURL" or key == "APPURL" or key == "INTERFACEURL":
                    if key == "INTERFACEURL":
                        continue
                    if key == "WANGSUURL" or key == "APPURL":
                        value = urllib2.unquote(value)
                        if key == "APPURL":
                            key = "localUrl"
                        else:
                            key = "url"
                    if key == "URL": key = "url"
                    spmatch = '{"regexp":{"' + key + '.keyword":".*' + value + '.*"}}'
                else:
                    spmatch = '{"regexp":{"' + key + '":".*' + value + '.*"}}'
                tiaojian.append(spmatch)
            elif type == "prefix":
                prefixmatch = '{"prefix":{"' + key + '":"' + value + '"}}'
                tiaojian.append(prefixmatch)
            elif type == "many":
                mtype = reqMjson[i]["mtype"]
                #valueArray = value.split(",")
                manymatch =  None
                if mtype == "s=":
                    #for valuetmp in valueArray:
                    #   manymatch = '{"term":{"' + key + '":"' + valuetmp + '"}}'
                    valuetmp = '"' + str(value.encode('utf-8')).replace(',','","') + '"'
                    manymatch = '{"terms":{"' + key.encode('utf-8') + ".keyword"'":[' + valuetmp + ']}}'
                elif mtype == "number":
                    manymatch = '{"terms":{"' + key + '":[' + value + ']}}'
                tiaojian.append(manymatch)

        result = '{"status":"200","msgs":"assemnble requirement successful"}'
        return result , tiaojian
    except:
        result = '{"status":"500","msgs":"assemnble requirement error"}'
        traceback.print_exc()
    return result , tiaojian

def assembleAGGS(aggs):
    '''
    aggs
    old aggs={"url":"url.keyword","st":"st","rport":"rport"}
    new aggs="url:url.keyword|st:st|rport:rport"
    '''
    aggsarray = aggs.split("|")
    for i in range(0 , len(aggsarray)):
        key = aggsarray[i][0:aggsarray[i].find(":")]
        #print "key" , key
        value = aggsarray[i][aggsarray[i].find(":")+1:len(aggsarray[i])]
        #print "value" , value
        #for key in aggs:
        tmpaggs = '"aggs":{"aggs_%s":{"terms":{"field": "%s","size":30},replace}}' %(key,value)
        if i == 0:
            aggsjson = tmpaggs
        else:
            aggsjson = aggsjson.replace("replace",tmpaggs)
    aggsjson = aggsjson.replace(",replace","")
    #return "{" + aggsjson + "}"
    return  aggsjson

def dateHistogramAvg(avgKey , startTimeStamp , endTimeStamp , countInt = "auto" , timeCol = "esDate" , interval = 60):
    if startTimeStamp > 9999999999:
        startTimeStamp = int(startTimeStamp) / 1000
    if endTimeStamp > 9999999999:
        endTimeStamp = int(endTimeStamp) / 1000
    rangeTime = endTimeStamp - startTimeStamp
    dateType = "HH:mm"
    if countInt == "auto":
        if rangeTime >=  60 * 60 * 24 and rangeTime < 60 * 60 * 24 * 2:
            interval = 60 * 60 * 2
            dateType = "MM-dd"
        elif rangeTime < 60 * 60 * 3 and rangeTime >= 60 * 60:
            interval = 60 * 3
        elif rangeTime < 60 * 60 * 12 and rangeTime >= 60 * 60 * 3:
            interval = 60 * 10
        elif rangeTime  < 60 * 60 * 24 and rangeTime >= 60 * 60 * 12:
            interval = 60 * 60
        elif rangeTime < 60 * 60 * 24 * 4 and rangeTime >= 60 * 60 * 24 * 2:
            interval = interval = 60 * 60 * 4
            dateType = "MM-dd"
        elif rangeTime < 60 * 60 * 24 * 6 and rangeTime >= 60 * 60 * 24 * 4:
            interval = interval = 60 * 60 * 6
            dateType = "MM-dd"
        elif rangeTime >= 60 * 60 * 24 * 6:
            interval = interval = 60 * 60 * 24
        elif rangeTime / 60 > 0:
            interval = 60
        else:
            interval = 1
    interTJ = '"aggs":{"rangeTime":{"date_histogram":{"field":"%s","interval":"%ss" ,  "time_zone":"+08:00"  , "format": "%s"},"aggs":{"options":{"avg":{"field":"%s"}}}}' % (timeCol , interval , dateType, avgKey)
    if str(avgKey).find("|") > 0:
        avgKey1 = str(avgKey)[0:str(avgKey).find("|")]
        avgKey2 = str(avgKey)[str(avgKey).find("|") + 1 : len(avgKey)]
        interTJ = '"aggs":{"rangeTime":{"date_histogram":{"field":"%s","interval":"%ss" , "time_zone":"+08:00" , "format": "%s"},"aggs":{"options":{"avg":{"field":"%s"}},"options2":{"avg":{"field":"%s"}}}}}' % (timeCol , interval , dateType, avgKey1 , avgKey2)
    return interTJ

if __name__ == "__main__":
    print  dateHistogramAvg("a|b" , 123456 , 123456)