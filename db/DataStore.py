#coding:utf-8
import sys
from config import DB_CONFIG
from util.exception import Con_DB_Fail


try:
    if DB_CONFIG['DB_CONNECT_TYPE'] == 'pymongo':
        from db.MongoHelper import MongoHelper as SqlHelper
    else:
        from db.SqlHelper import SqlHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
except Exception,e:
    raise Con_DB_Fail


def store_data(queue2,db_proxy_num):
    '''
    读取队列中的数据，写入数据库中
    :param queue2:
    :return:
    '''
    successNum = 0
    failNum = 0
    while True:
        try:
            proxy = queue2.get(timeout=300)
            if proxy:

                sqlhelper.insert(proxy)
                successNum += 1
            else:
                failNum += 1
            str = u'IPProxyPool----->>>>>>>>Success ip num :%d,Fail ip num:%d' % (successNum,failNum)
            sys.stdout.write(str+"\r")
            sys.stdout.flush()
        except BaseException,e:

            if db_proxy_num.value != 0:
                successNum += db_proxy_num.value
                db_proxy_num.value=0
                str = u'IPProxyPool----->>>>>>>>Success ip num :%d,Fail ip num:%d' % (successNum,failNum)
                sys.stdout.write(str+"\r")
                sys.stdout.flush()
                successNum = 0
                failNum = 0


