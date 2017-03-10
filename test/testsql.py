# coding:utf-8
from db.SqlHelper import SqlHelper
from util.exception import Con_DB_Fail

try:
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
except Exception:
    raise Con_DB_Fail

proxy = {'ip': '192.168.1.1', 'port': int('80'), 'type': 0, 'protocol': 0, 'country': u'中国', 'area': u'四川', 'speed': 0}
sqlhelper.insert(proxy)