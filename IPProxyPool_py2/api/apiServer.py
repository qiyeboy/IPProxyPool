# coding:utf-8
'''
定义几个关键字，count type,protocol,country,area,
'''
import json
import sys
import web
import config
from db.DataStore import sqlhelper
from db.SqlHelper import Proxy

urls = (
    '/', 'select',
    '/delete', 'delete'
)


def start_api_server():
    sys.argv.append('0.0.0.0:%s' % config.API_PORT)
    app = web.application(urls, globals())
    app.run()


class select(object):
    def GET(self):
        inputs = web.input()
        json_result = json.dumps(sqlhelper.select(inputs.get('count', None), inputs))
        return json_result


class delete(object):
    params = {}

    def GET(self):
        inputs = web.input()
        json_result = json.dumps(sqlhelper.delete(inputs))
        return json_result


if __name__ == '__main__':
    sys.argv.append('0.0.0.0:8000')
    app = web.application(urls, globals())
    app.run()
