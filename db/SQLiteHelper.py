#coding:utf-8
from config import DB_CONFIG
from db.SqlHelper import SqlHelper

__author__ = 'Xaxdus'
import sqlite3
class SqliteHelper(SqlHelper):

    tableName='proxys'
    def __init__(self):
        '''
        建立数据库的链接
        :return:
        '''
        self.database = sqlite3.connect(DB_CONFIG['dbPath'],check_same_thread=False)
        self.cursor = self.database.cursor()
        #创建表结构
        self.createTable()
    def compress(self):
        '''
        数据库进行压缩
        :return:
        '''
        self.database.execute('VACUUM')

    def createTable(self):
        self.cursor.execute("create TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY ,ip VARCHAR(16) NOT NULL,"
               "port INTEGER NOT NULL ,types INTEGER NOT NULL ,protocol INTEGER NOT NULL DEFAULT 0,"
               "country VARCHAR (20) NOT NULL,area VARCHAR (20) NOT NULL,updatetime TimeStamp NOT NULL DEFAULT (datetime('now','localtime')) ,speed DECIMAL(3,2) NOT NULL DEFAULT 100)"% self.tableName)

        self.database.commit()

    def select(self,tableName,condition,count):
        '''

        :param tableName: 表名
        :param condition: 条件包含占位符
        :param value:  占位符所对应的值(主要是为了防注入)
        :return:
        '''
        command = 'SELECT DISTINCT ip,port FROM %s WHERE %s ORDER BY speed ASC %s '%(tableName,condition,count)

        self.cursor.execute(command)
        result = self.cursor.fetchall()
        return result

    def selectAll(self):
        self.cursor.execute('SELECT DISTINCT ip,port FROM %s ORDER BY speed ASC '%self.tableName)
        result = self.cursor.fetchall()
        return result

    def selectCount(self):
        self.cursor.execute('SELECT COUNT( DISTINCT ip) FROM %s'%self.tableName)
        count = self.cursor.fetchone()
        return count

    def selectOne(self,tableName,condition,value):
        '''

        :param tableName: 表名
        :param condition: 条件包含占位符
        :param value:  占位符所对应的值(主要是为了防注入)
        :return:
        '''
        self.cursor.execute('SELECT DISTINCT ip,port FROM %s WHERE %s ORDER BY speed ASC'%(tableName,condition),value)
        result = self.cursor.fetchone()
        return result

    def update(self,tableName,condition,value):
        self.cursor.execute('UPDATE %s %s'%(tableName,condition),value)
        self.database.commit()

    def delete(self,tableName,condition):
        '''

        :param tableName: 表名
        :param condition: 条件
        :return:
        '''
        deleCommand = 'DELETE FROM %s WHERE %s'%(tableName,condition)
        # print deleCommand
        self.cursor.execute(deleCommand)
        self.commit()

    def commit(self):
        self.database.commit()


    def insert(self,tableName,value):

        proxy = [value['ip'],value['port'],value['type'],value['protocol'],value['country'],value['area'],value['speed']]
        # print proxy
        self.cursor.execute("INSERT INTO %s (ip,port,types,protocol,country,area,speed)VALUES (?,?,?,?,?,?,?)"% tableName
                            ,proxy)


    def batch_insert(self,tableName,values):

        for value in values:
            if value!=None:
                self.insert(self.tableName,value)
        self.database.commit()


    def close(self):
        self.cursor.close()
        self.database.close()



if __name__=="__main__":
    s = SqliteHelper()
    print s.selectCount()[0]
    # print s.selectAll()