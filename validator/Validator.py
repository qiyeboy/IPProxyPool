#coding:utf-8
import datetime
from gevent.pool import Pool
import requests
import time
from config import TEST_URL
import config
from db.SQLiteHelper import SqliteHelper
from gevent import monkey
monkey.patch_all()
__author__ = 'Xaxdus'

class Validator(object):

    def __init__(self):
        self.detect_pool = Pool(config.THREADNUM)


    def __init__(self,sqlHelper):
        self.detect_pool = Pool(config.THREADNUM)
        self.sqlHelper =sqlHelper


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
            print e
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

            if not r.ok:
                condition = "ip='"+ip+"' AND "+'port='+port
                print 'fail ip =%s'%ip
                self.sqlHelper.delete(SqliteHelper.tableName,condition)
            else:
                speed = round(time.time()-start, 2)
                self.sqlHelper.update(SqliteHelper.tableName,'SET speed=? WHERE ip=? AND port=?',(speed,ip,port))
                print 'success ip =%s,speed=%s'%(ip,speed)
        except Exception,e:
                condition = "ip='"+ip+"' AND "+'port='+port
                print 'fail ip =%s'%ip
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
        start = time.time()
        try:
            r = requests.get(url=TEST_URL,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)

            if not r.ok:
                print 'fail ip =%s'%ip
                proxy = None

            else:
                speed = round(time.time()-start,2)
                print 'success ip =%s,speed=%s'%(ip,speed)
                proxy['speed']=speed
                # return proxy
        except Exception,e:
                print 'fail ip =%s'%ip
                proxy = None
        return proxy
        # return proxys


if __name__=='__main__':
    # v = Validator()
    # results=[{'ip':'192.168.1.1','port':80}]*10
    # results = v.run(results)
    # print results
    pass
