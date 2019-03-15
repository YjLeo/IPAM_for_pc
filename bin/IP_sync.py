# coding=utf-8
import os
import sys

from core.Connect import redis
from core.IPinit import search_pod_health, len_allocat, clean_redis, search_k8s, search_DB, Sync_idmap

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import iptc

if __name__ == '__main__':
     print "开始健康检查"
     search_pod_health()
     print "K8S系统正常"
     if len_allocat()>=1500:
          print "IP余量大于1500不进行初始化:"+str(len_allocat())
     else:
          print "开始关闭端口"


          table = iptc.Table(iptc.Table.FILTER)
          chain = iptc.Chain(table, "INPUT")
          rule = iptc.Rule()
          rule.protocol = "tcp"
          match = iptc.Match(rule, 'tcp')
          rule.add_match(match)
          match.dport='5000'
          target = rule.create_target("DROP")
          rule.target = target
          chain.insert_rule(rule)
          table.commit()


          print  "##清空队列所有cache"
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
          Sync_idmap()
          print "释放端口"



         #########################
          chain.delete_rule(rule)
          table.commit()









