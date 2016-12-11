#coding:utf-8
from multiprocessing import Value, Queue, Process
from api.apiServer import start_api_server
import sys
from db.DataStore import store_data
from spider.ProxyCrawl import startProxyCrawl
from validator.Validator import validator
#import imp
#imp.reload(sys)
#sys.setdefaultencoding('utf8')




if __name__=="__main__":
    DB_PROXY_NUM=Value('i',0)
    q1 = Queue()
    q2 = Queue()
    p0 = Process(target=start_api_server)
    p1 = Process(target=startProxyCrawl,args=(q1,DB_PROXY_NUM))
    p2 = Process(target=validator,args=(q1,q2))
    p3 = Process(target=store_data,args=(q2,DB_PROXY_NUM))
    p0.start()
    p1.start()
    p2.start()
    p3.start()






