#coding:utf-8
from gevent.pool import Pool
import requests
import time
from config import THREADNUM, parserList, MINNUM, UPDATE_TIME
from db.SQLiteHelper import SqliteHelper
from spider.HtmlDownLoader import Html_Downloader
from spider.HtmlPraser import Html_Parser
from validator.Validator import Validator


__author__ = 'Xaxdus'
from gevent import monkey
monkey.patch_all()
'''
这个类的作用是描述爬虫的逻辑
'''
class ProxySpider(object):

    def __init__(self):
        self.crawl_pool = Pool(THREADNUM)
        # self.sqlHelper = sqlHelper

    def run(self):
        while True:
            print 'spider beginning -------'
            sqlHelper = SqliteHelper()
            print 'validator beginning -------'
            validator = Validator(sqlHelper)
            count = validator.run_db()
            print 'validator end ----count=%s'%count
            if count[0]< MINNUM:
                proxys = self.crawl_pool.map(self.crawl,parserList)
                #这个时候proxys的格式是[[{},{},{}],[{},{},{}]]
                # print proxys
                #这个时候应该去重:

                proxys_tmp = []
                for proxy in proxys:
                    proxys_tmp.extend(proxy)

                proxys = proxys_tmp
                print 'first_proxys--%s',len(proxys)
                #这个时候proxys的格式是[{},{},{},{},{},{}]
                proxys_tmp=None
                #这个时候开始去重:
                proxys = [dict(t) for t in set([tuple(proxy.items()) for proxy in proxys])]
                print 'end_proxys--%s',len(proxys)
                print 'spider proxys -------%s'%type(proxys)
                proxys = validator.run_list(proxys)#这个是检测后的ip地址


                sqlHelper.batch_insert(sqlHelper.tableName,proxys)


                print 'success ip =%s'%sqlHelper.selectCount()
                sqlHelper.close()
            print 'spider end -------'
            time.sleep(UPDATE_TIME)


    def crawl(self,parser):
        proxys = []
        html_parser = Html_Parser()
        for url in parser['urls']:
           response = Html_Downloader.download(url)
           # print response
           if response!=None:
               proxylist= html_parser.parse(response,parser)
               if proxylist != None:
                  proxys.extend(proxylist)
        return proxys


if __name__=="__main__":
    spider = ProxySpider()
    spider.run()