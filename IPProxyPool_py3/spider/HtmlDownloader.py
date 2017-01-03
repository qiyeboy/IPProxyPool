#coding:utf-8

import random
import config
import json
from db.DataStore import sqlhelper

__author__ = 'qiye'

import requests
import chardet
class Html_Downloader(object):

    @classmethod
    def download(self,url):
        count = 0#重试次数
        r=''
        try:
            r = requests.get(url=url,headers=config.HEADER,timeout=config.TIMEOUT)
            r.encoding =chardet.detect(r.content)['encoding']
            while count< config.RETRY_TIME:
                if (not r.ok) or len(r.content)<500 :
                    proxylist = sqlhelper.select(10)
                    proxy = random.choice(proxylist)
                    ip = proxy[0]
                    port = proxy[1]
                    proxies={"http": "http://%s:%s"%(ip,port),"https": "http://%s:%s"%(ip,port)}
                    try:
                        r = requests.get(url=url,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)
                        r.encoding =chardet.detect(r.content)['encoding']
                        count += 1
                    except Exception as e:
                         count += 1


                else:
                    return r.text

            return None

        except Exception as e:
            while count< config.RETRY_TIME:
                if r==''or (not r.ok) or len(r.content)<500 :
                    try:
                        proxylist = sqlhelper.select(10)
                        proxy = random.choice(proxylist)
                        ip = proxy[0]
                        port = proxy[1]
                        proxies={"http": "http://%s:%s"%(ip,port),"https": "http://%s:%s"%(ip,port)}
                        try:
                            r = requests.get(url=url,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)
                            r.encoding =chardet.detect(r.content)['encoding']
                            count += 1
                        except Exception as e:
                             count += 1

                    except Exception as e:
                        return None

                else:
                    return r.text

            return None









