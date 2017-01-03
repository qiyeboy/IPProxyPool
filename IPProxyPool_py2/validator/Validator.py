#coding:utf-8
import json
from multiprocessing import Process
import re
import gevent

from lxml import etree
import requests
import time
from config import TEST_URL
import config
from db.DataStore import sqlhelper
from util.exception import Test_URL_Fail



from gevent import monkey
monkey.patch_all()


def detect_from_db(myip,proxy,proxies_set):
    proxy_dict = {'ip':proxy[0],'port':proxy[1]}
    result = detect_list(myip,proxy_dict)
    if result:
        if proxy[2]<60000:
            score = proxy[2] + 1
        else:
            score = 60000
        proxy_str ='%s:%s'%(proxy[0],proxy[1])
        proxies_set.add(proxy_str)
        sqlhelper.update({'ip':proxy[0],'port':proxy[1]},{'score':score})
    else:
        sqlhelper.delete({'ip':proxy[0],'port':proxy[1]})


    pass


def validator(queue1,queue2):
    tasklist=[]
    myip = getMyIP()
    while True:
        try:
            # proxy_dict = {'source':'crawl','data':proxy}
            proxy = queue1.get(timeout=10)
            tasklist.append(proxy)
            if len(tasklist)>500:
                p = Process(target=process_start,args=(tasklist,myip,queue2))
                p.start()
                tasklist=[]
        except Exception,e:
            if len(tasklist)>0:
                p = Process(target=process_start,args=(tasklist,myip,queue2))
                p.start()
                tasklist=[]


def process_start(tasks,myip,queue2):
    spawns = []
    for task in tasks:
        spawns.append(gevent.spawn(detect_list,myip,task,queue2))
    gevent.joinall(spawns)


def detect_list(selfip,proxy,queue2=None):
    '''
    :param proxy: ip字典
    :return:
    '''
    ip = proxy['ip']
    port = proxy['port']
    proxies={"http": "http://%s:%s"%(ip,port),"https": "http://%s:%s"%(ip,port)}
    # proxyType = checkProxyType(selfip,proxies)
    # if proxyType==3:
    #     logger.info('failed %s:%s'%(ip,port))
    #     proxy = None
    #     queue2.put(proxy)
    #     return proxy
    # else:
    #     proxy['type']=proxyType
    proxy['type']=0
    start = time.time()
    try:
        r = requests.get(url=TEST_URL,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)

        if not r.ok or r.text.find(ip)==-1:
            proxy = None
        else:
            speed = round(time.time()-start,2)
            proxy['speed']=speed
    except Exception,e:
            proxy = None

    if queue2:
        queue2.put(proxy)
    return proxy

def checkProxyType(selfip,proxies):
    '''
    用来检测代理的类型，突然发现，免费网站写的信息不靠谱，还是要自己检测代理的类型
    :param proxies: 代理(0 高匿，1 匿名，2 透明 3 无效代理
    :return:
    '''

    try:

        r = requests.get(url=config.TEST_PROXY,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)
        if r.ok:
            root = etree.HTML(r.text)
            ip = root.xpath('.//center[2]/table/tr[3]/td[2]')[0].text
            http_x_forwared_for = root.xpath('.//center[2]/table/tr[8]/td[2]')[0].text
            http_via = root.xpath('.//center[2]/table/tr[9]/td[2]')[0].text
            # print ip,http_x_forwared_for,http_via,type(http_via),type(http_x_forwared_for)
            if ip==selfip:
                return 3
            if http_x_forwared_for is None and http_via is None:
                return 0
            if http_via != None and http_x_forwared_for.find(selfip)== -1:
                return 1

            if http_via != None and http_x_forwared_for.find(selfip)!= -1:
                return 2
        return 3



    except Exception,e:
        return 3




def getMyIP():
    try:
        r = requests.get(url=config.TEST_URL,headers=config.HEADER,timeout=config.TIMEOUT)
        pattern = '\d+\.\d+\.\d+\.\d+'
        match =re.search(pattern,r.text)
        if match:
            ip = match.group()
            return ip
        else:

            raise Test_URL_Fail
    except Exception,e:
            raise Test_URL_Fail

if __name__=='__main__':
    getMyIP()
    # str="{ip:'61.150.43.121',address:'陕西省西安市 西安电子科技大学'}"
    # j = json.dumps(str)
    # str = j['ip']
    # print str