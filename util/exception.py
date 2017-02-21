# coding:utf-8
import config


class Test_URL_Fail(Exception):
    def __str__(self):
        str = "访问%s失败，请检查网络连接" % config.TEST_IP
        return str


class Con_DB_Fail(Exception):
    def __str__(self):
        str = "使用DB_CONNECT_STRING:%s--连接数据库失败" % config.DB_CONNECT_STRING
        return str
