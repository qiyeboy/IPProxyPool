# coding:utf-8
from redis import Redis

import config
from db.ISqlHelper import ISqlHelper
from db.SqlHelper import Proxy


class RedisHelper(ISqlHelper):
    def __init__(self, url=None):
        self.index_names = ('types', 'protocol', 'country', 'area')
        self.redis_url = url or config.DB_CONFIG['DB_CONNECT_STRING']

    def get_proxy_name(self, ip=None, port=None, protocal=None, proxy=None):
        ip = ip or proxy.ip
        port = port or proxy.port
        protocal = protocal or proxy.protocol
        return "proxy::{}:{}:{}".format(ip, port, protocal)

    def get_index_name(self, index_name, value):
        return "index::{}:{}".format(index_name, value)

    def get_proxy_by_name(self, name):
        pd = self.redis.hgetall(name)
        if pd:
            return Proxy(**{k.decode('utf8'): v.decode('utf8') for k, v in pd.items()})

    def init_db(self, url=None):
        self.redis = Redis.from_url(url or self.redis_url)

    def drop_db(self):
        return self.redis.flushdb()

    def get_keys(self, conditions):
        select_keys = {}
        for key in conditions.keys():
            if key in self.index_names:
                select_keys[key] = conditions[key]
        skeys = [self.get_index_name(k, v) for k, v in select_keys.items()]
        return self.redis.sinter(keys=skeys)

    def insert(self, value):
        proxy = Proxy(ip=value['ip'], port=value['port'], types=value['types'], protocol=value['protocol'],
                      country=value['country'],
                      area=value['area'], speed=value['speed'], score=0)
        mapping = proxy.__dict__
        for k in list(mapping.keys()):
            if k.startswith('_'):
                mapping.pop(k)
        object_name = self.get_proxy_name(proxy=proxy)
        # 存结构
        self.redis.hmset(object_name, mapping)
        # 创建索引
        for name in self.index_names:
            index_key = self.get_index_name(name, value[name])
            self.redis.sadd(index_key, object_name)

    def delete(self, conditions):
        proxy_keys = self.get_keys(conditions)
        index_keys = self.redis.keys("index::*")
        for iname in index_keys:
            for pname in proxy_keys:
                self.redis.srem(iname, pname)
        return self.redis.delete(*proxy_keys) if proxy_keys else 0

    def update(self, conditions, values):
        objects = self.get_keys(conditions)
        count = 0
        for name in objects:
            for k, v in values.items():
                self.redis.hset(name, key=k, value=v)
            count += 1
        return count

    def select(self, count=None, conditions=None):
        result = []
        if conditions:
            objects = self.get_keys(conditions)
        else:
            objects = self.redis.keys('proxy::*')
        for name in objects[:count]:
            p = self.get_proxy_by_name(name)
            result.append((p.ip, p.port, p.score))
        return result


if __name__ == '__main__':
    sqlhelper = RedisHelper()
    sqlhelper.init_db('redis://localhost:6379/66')
    proxy = {'ip': '192.168.1.1', 'port': 80, 'type': 0, 'protocol': 0, 'country': '中国', 'area': '广州', 'speed': 11.123,
             'types': 1}
    sqlhelper.insert(proxy)
    print(sqlhelper.select(conditions={'types': 1}))
    print(sqlhelper.update({'types': 1}, {'port': 433}))
    print(sqlhelper.delete({'types': 1}))
    print(sqlhelper.select(1))
    sqlhelper.drop_db()
