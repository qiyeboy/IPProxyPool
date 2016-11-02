#coding:utf-8
from gevent.pool import Pool
import requests
import time
from config import THREADNUM, parserList, MINNUM, UPDATE_TIME
from db.SQLiteHelper import SqliteHelper
from spider.HtmlDownLoader import Html_Downloader
from spider.HtmlPraser import Html_Parser
from validator.Validator import Validator
import logging
logger = logging.getLogger('spider')

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
            logger.info("Start to run spider")
            sqlHelper = SqliteHelper()
            logger.info('Start to run validator')
            validator = Validator(sqlHelper)
            count = validator.run_db()
            logger.info('Finished to run validator, count=%s'%count)
            if count[0]< MINNUM:
                proxys = self.crawl_pool.map(self.crawl,parserList)
                #这个时候proxys的格式是[[{},{},{}],[{},{},{}]]
                # print proxys
                #这个时候应该去重:

                proxys_tmp = []
                for proxy in proxys:
                    proxys_tmp.extend(proxy)

                proxys = proxys_tmp
                logger.info('first_proxys: %s'%len(proxys))
                #这个时候proxys的格式是[{},{},{},{},{},{}]
                proxys_tmp=None
                #这个时候开始去重:
                proxys = [dict(t) for t in set([tuple(proxy.items()) for proxy in proxys])]
                logger.info('end_proxy: %s'%len(proxys))
                logger.info('spider proxys: %s'%type(proxys))
                proxys = validator.run_list(proxys)#这个是检测后的ip地址

                sqlHelper.batch_insert(sqlHelper.tableName,proxys)

                logger.info('success ip: %s'%sqlHelper.selectCount())
                sqlHelper.close()
            logger.info('Finished to run spider')
            time.sleep(UPDATE_TIME)


    def crawl(self,parser):
        proxys = []
        html_parser = Html_Parser()
        for url in parser['urls']:
           response = Html_Downloader.download(url)
           if response!=None:
               proxylist= html_parser.parse(response,parser)
               if proxylist != None:
                  proxys.extend(proxylist)
        return proxys


if __name__=="__main__":
    spider = ProxySpider()
    spider.run()