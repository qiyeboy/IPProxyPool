#coding:utf-8
import datetime

from lxml import etree
from gevent.pool import Pool
import requests
import time
from config import TEST_URL
import config
from db.SQLiteHelper import SqliteHelper
import logging
logger = logging.getLogger("validator")

from gevent import monkey
monkey.patch_all()


__author__ = 'Xaxdus'

class Validator(object):

    def __init__(self,sqlHelper):

        self.detect_pool = Pool(config.THREADNUM)
        self.sqlHelper =sqlHelper
        self.selfip = self.getMyIP()
        self.detect_pool = Pool(config.THREADNUM)

    def run_db(self):
        '''
        从数据库中检测
        :return:
        '''
        try:
            #首先将超时的全部删除
            self.deleteOld()
            #接着检测剩余的ip,是否可用
            results = self.sqlHelper.selectAll()
            self.detect_pool.map(self.detect_db,results)
            #将数据库进行压缩
            self.sqlHelper.compress()

            return self.sqlHelper.selectCount()#返回最终的数量
        except Exception,e:
            logger.warning(str(e))
            return 0



    def run_list(self,results):
        '''
        这个是先不进入数据库，直接从集合中删除
        :param results:
        :return:
        '''
        # proxys=[]
        # for result in results:
        proxys = self.detect_pool.map(self.detect_list,results)
        #这个时候proxys的格式是[{},{},{},{},{}]
        return proxys

    def deleteOld(self):
        '''
        删除旧的数据
        :return:
        '''
        condition = "updatetime<'%s'"%((datetime.datetime.now() - datetime.timedelta(minutes=config.MAXTIME)).strftime('%Y-%m-%d %H:%M:%S'))
        self.sqlHelper.delete(SqliteHelper.tableName,condition)


    def detect_db(self,result):
        '''

        :param result: 从数据库中检测
        :return:
        '''
        ip = result[0]
        port = str(result[1])
        proxies={"http": "http://%s:%s"%(ip,port)}

        start = time.time()
        try:
            r = requests.get(url=TEST_URL,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)

            if not r.ok or r.text.find(ip)==-1:
                condition = "ip='"+ip+"' AND "+'port='+port
                logger.info('failed %s:%s'%(ip,port))
                self.sqlHelper.delete(SqliteHelper.tableName,condition)
            else:
                logger.info(r.text)
                speed = round(time.time()-start, 2)
                self.sqlHelper.update(SqliteHelper.tableName,'SET speed=? WHERE ip=? AND port=?',(speed,ip,port))
                logger.info('success %s:%s, speed=%s'%(ip,port,speed))
        except Exception,e:
                condition = "ip='"+ip+"' AND "+'port='+port
                logger.info('failed %s:%s'%(ip,port))
                self.sqlHelper.delete(SqliteHelper.tableName,condition)



    def detect_list(self,proxy):
        '''
        :param proxy: ip字典
        :return:
        '''
        # for proxy in proxys:

        ip = proxy['ip']
        port = proxy['port']
        proxies={"http": "http://%s:%s"%(ip,port)}
        proxyType = self.checkProxyType(proxies)
        if proxyType==3:
            logger.info('failed %s:%s'%(ip,port))

            proxy = None
            return proxy
        else:
            proxy['type']=proxyType
        start = time.time()
        try:
            r = requests.get(url=TEST_URL,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)

            if not r.ok or r.text.find(ip)==-1:
                logger.info('failed %s:%s'%(ip,port))
                proxy = None
            else:
                speed = round(time.time()-start,2)
                logger.info('success %s:%s, speed=%s'%(ip,port,speed))
                proxy['speed']=speed
                # return proxy
        except Exception,e:
                logger.info('failed %s:%s'%(ip,port))
                proxy = None
        return proxy
        # return proxys

    def checkProxyType(self,proxies):
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
                if ip==self.selfip:
                    return 3
                if http_x_forwared_for is None and http_via is None:
                    return 0
                if http_via != None and http_x_forwared_for.find(self.selfip)== -1:
                    return 1

                if http_via != None and http_x_forwared_for.find(self.selfip)!= -1:
                    return 2
            return 3



        except Exception,e:
            logger.warning(str(e))
            return 3



    def getMyIP(self):
        try:
            r = requests.get(url=config.TEST_PROXY,headers=config.HEADER,timeout=config.TIMEOUT)
            # print r.text
            root = etree.HTML(r.text)
            ip = root.xpath('.//center[2]/table/tr[3]/td[2]')[0].text

            logger.info('ip %s' %ip)
            return ip
        except Exception,e:
            logger.info(str(e))
            return None

if __name__=='__main__':
    v = Validator(None)
    v.getMyIP()
    v.selfip
    # results=[{'ip':'192.168.1.1','port':80}]*10
    # results = v.run(results)
    # print results
    pass
