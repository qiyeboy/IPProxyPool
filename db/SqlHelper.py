#coding:utf-8

__author__ = 'Xaxdus'
'''
sql操作的基类
包括ip，端口，types类型(0高匿名，1透明)，protocol(0 http,1 https http),country(国家),area(省市),updatetime(更新时间)
 speed(连接速度)
'''
class SqlHelper(object):



    def __init__(self):
        pass

    def insert(self,value):
        pass

    def batch_insert(self,values):
        pass

    def delete(self,condition):
        pass

    def batch_delete(self,values):
        pass

    def update(self,condition,value):
        pass
    def select(self,condition):
        pass
    def selectOne(self,tableName,condition,value):
        pass
    def close(self):
        pass
