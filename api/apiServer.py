#coding:utf-8
'''
定义几个关键字，count type,protocol,country,area,
'''
import urllib
from config import API_PORT
from db.SQLiteHelper import SqliteHelper

__author__ = 'Xaxdus'

import BaseHTTPServer
import json
import urlparse

# keylist=['count', 'types','protocol','country','area']
class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        """
        """
        dict={}

        parsed_path = urlparse.urlparse(self.path)
        try:
            query = urllib.unquote(parsed_path.query)
            print query
            if query.find('&')!=-1:
                params = query.split('&')
                for param in params:
                    dict[param.split('=')[0]]=param.split('=')[1]
            else:
                    dict[query.split('=')[0]]=query.split('=')[1]
            str_count=''
            conditions=[]
            for key in dict:
                if key =='count':
                    str_count = 'lIMIT 0,%s'% dict[key]
                if key =='country' or key =='area':
                    conditions .append(key+" LIKE '"+dict[key]+"%'")
                elif key =='types' or key =='protocol' or key =='country' or key =='area':
                    conditions .append(key+"="+dict[key])
            if len(conditions)>1:
                conditions = ' AND '.join(conditions)
            else:
                conditions =conditions[0]
            sqlHelper = SqliteHelper()
            result = sqlHelper.select(sqlHelper.tableName,conditions,str_count)
            # print type(result)
            # for r in  result:
            #     print r
            print result
            data = json.dumps(result)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(data)
        except Exception,e:
            print e
            self.send_response(404)

if __name__=='__main__':
    server = BaseHTTPServer.HTTPServer(('0.0.0.0',API_PORT), WebRequestHandler)
    server.serve_forever()