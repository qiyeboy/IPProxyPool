# coding:utf-8
from lxml import etree
import requests
import config


def checkProxyType(selfip, proxies):
    '''
    用来检测代理的类型，突然发现，免费网站写的信息不靠谱，还是要自己检测代理的类型
    :param proxies: 代理(0 高匿，1 匿名，2 透明 3 无效代理
    :return:
    '''

    try:
        r = requests.get(url='https://incloak.com/ip/', headers=config.HEADER, timeout=config.TIMEOUT, proxies=proxies)
        print
        r.text
        # if r.ok:
        # root = etree.HTML(r.text)
        # ip = root.xpath('.//center[2]/table/tr[3]/td[2]')[0].text
        # http_x_forwared_for = root.xpath('.//center[2]/table/tr[8]/td[2]')[0].text
        #     http_via = root.xpath('.//center[2]/table/tr[9]/td[2]')[0].text
        #     # print ip,http_x_forwared_for,http_via,type(http_via),type(http_x_forwared_for)
        #     if ip==selfip:
        #         return 3
        #     if http_x_forwared_for is None and http_via is None:
        #         return 0
        #     if http_via != None and http_x_forwared_for.find(selfip)== -1:
        #         return 1
        #
        #     if http_via != None and http_x_forwared_for.find(selfip)!= -1:
        #         return 2
        # return 3


    except Exception as e:
        print
        str(e)
        return 3


if __name__ == '__main__':
    ip = '61.132.241.109'
    port = '808'
    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}
    checkProxyType(None, proxies)