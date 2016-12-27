# coding: utf-8
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
except Exception, e:
    raise Con_DB_Fail


def store_data(useful_proxys_queue, db_proxy_num, faild_ip_num):
    '''
    读取队列中的数据，写入数据库中
    :param useful_proxys_queue:
    :return:
    '''
    successNum = 0
    while True:
        if db_proxy_num.value:
            successNum = db_proxy_num.value
            db_proxy_num.value = 0
        try:
            proxy = useful_proxys_queue.get(timeout=3000)
            if proxy:
                sqlhelper.insert(proxy)
                successNum += 1
            str = u'IPProxyPool----->>>>>>>>Success ip num :%d,Fail ip num:%d' % (
                successNum, faild_ip_num.value)
            sys.stdout.write(str + "\r")
            sys.stdout.flush()
        except BaseException, e:
            continue
