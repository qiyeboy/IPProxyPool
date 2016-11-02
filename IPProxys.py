#coding:utf-8
import BaseHTTPServer
import threading
import logging
import logging.config

from api.apiServer import WebRequestHandler
from config import API_PORT
from db.SQLiteHelper import SqliteHelper
from spider.ProxySpider import ProxySpider

logging.config.fileConfig('logging.conf')

class IPProxys(object):

    def startApiServer(self):
        '''
        启动api服务器
        :return:
        '''
        logging.info('Start server @ %s:%s' %('0.0.0.0',API_PORT))
        server = BaseHTTPServer.HTTPServer(('0.0.0.0',API_PORT), WebRequestHandler)
        server.serve_forever()

    def startSpider(self):
        logging.info('Start Spider')
        spider = ProxySpider()
        spider.run()

if __name__=="__main__":

    proxys = IPProxys()

    apiServer = threading.Thread(target=proxys.startApiServer)
    spider = threading.Thread(target=proxys.startSpider)
    apiServer.start()
    spider.start()






