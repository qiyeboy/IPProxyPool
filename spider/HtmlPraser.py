#coding:utf-8
import datetime
from config import QQWRY_PATH, CHINA_AREA

from util.IPAddress import IPAddresss
from util.logger import logger

__author__ = 'Xaxdus'
from lxml import etree
class Html_Parser(object):

    def __init__(self):
        self.ips = IPAddresss(QQWRY_PATH)
    def parse(self,response,parser):
        '''

        :param response: 响应
        :param type: 解析方式
        :return:
        '''
        if parser['type']=='xpath':
            proxylist=[]
            root = etree.HTML(response)
            proxys = root.xpath(parser['pattern'])
            for proxy in proxys:
                # print parser['postion']['ip']
                ip = proxy.xpath(parser['postion']['ip'])[0].text
                port = proxy.xpath(parser['postion']['port'])[0].text
                type = proxy.xpath(parser['postion']['type'])[0].text
                if type.find(u'高匿')!=-1:
                    type = 0
                else:
                    type = 1
                protocol=''
                if len(parser['postion']['protocol']) > 0:
                    protocol = proxy.xpath(parser['postion']['protocol'])[0].text
                    if protocol.lower().find('https')!=-1:
                        protocol = 1
                    else:
                        protocol = 0
                else:
                    protocol = 0
                addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                country = ''
                area = ''
                if addr.find(u'省')!=-1 or self.AuthCountry(addr):
                    country = u'中国'
                    area = addr
                else:
                    country = addr
                    area = ''
                # updatetime = datetime.datetime.now()
                # ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https http),country(国家),area(省市),updatetime(更新时间)

                # proxy ={'ip':ip,'port':int(port),'type':int(type),'protocol':int(protocol),'country':country,'area':area,'updatetime':updatetime,'speed':100}
                proxy ={'ip':ip,'port':int(port),'type':int(type),'protocol':int(protocol),'country':country,'area':area,'speed':100}
                print proxy
                proxylist.append(proxy)

            return proxylist

    def AuthCountry(self,addr):
        '''
        用来判断地址是哪个国家的
        :param addr:
        :return:
        '''
        for area in CHINA_AREA:
            if addr.find(area)!=-1:
                return True
        return False














