#coding:utf-8
import datetime
from config import QQWRY_PATH, CHINA_AREA

from util.IPAddress import IPAddresss
import re
import logging
logger = logging.getLogger('spider')

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
            return self.XpathPraser(response,parser)
        elif parser['type']=='regular':
            return self.RegularPraser(response,parser)
        elif parser['type']=='module':
            return getattr(self,parser['moduleName'],None)(response,parser)
        else:
            return None

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



    def XpathPraser(self,response,parser):
        '''
        针对xpath方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist=[]
        root = etree.HTML(response)
        proxys = root.xpath(parser['pattern'])
        for proxy in proxys:
            # print parser['postion']['ip']
            try:
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
            except Exception,e:
                continue
            # updatetime = datetime.datetime.now()
            # ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https http),country(国家),area(省市),updatetime(更新时间)

            # proxy ={'ip':ip,'port':int(port),'type':int(type),'protocol':int(protocol),'country':country,'area':area,'updatetime':updatetime,'speed':100}
            proxy ={'ip':ip,'port':int(port),'type':int(type),'protocol':int(protocol),'country':country,'area':area,'speed':100}
            logger.info("Fetch proxy %s" %str(proxy))
            proxylist.append(proxy)

        return proxylist

    def RegularPraser(self,response,parser):
        '''
        针对正则表达式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist=[]
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs !=None:
            for match in matchs:
                logging.info(str(match))
                ip = match[parser['postion']['ip']]
                port = match[parser['postion']['port']]
                #网站的类型一直不靠谱所以还是默认，之后会检测
                type =0
                if parser['postion']['protocol'] > 0:
                    protocol = match[parser['postion']['protocol']]
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
                proxy ={'ip':ip,'port':port,'type':type,'protocol':protocol,'country':country,'area':area,'speed':100}
                logger.info("Fetch proxy %s" % str(proxy))
                proxylist.append(proxy)
            return proxylist


    def CnproxyPraser(self,response,parser):
        proxylist = self.RegularPraser(response,parser)
        chardict ={'v':'3','m':'4','a':'2','l':'9','q':'0','b':'5','i':'7','w':'6','r':'8','c':'1'}

        for proxy in proxylist:
            port = proxy['port']
            new_port = ''
            for i in range(len(port)):
                if port[i]!='+':
                   new_port += chardict[port[i]]
            new_port = int(new_port)
            proxy['port'] =new_port
        return proxylist








