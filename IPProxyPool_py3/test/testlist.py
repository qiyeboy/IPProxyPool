# coding:utf-8
from decimal import Decimal

__author__ = 'Xaxdus'


# list = ["www.baidu.com/%s" %m for m in ['index']+range(1,5)]
#
# list = [(1,10)]*10
#
# for m,n in list:
# print m,n
#
#
# list2 = ["www.baidu.com/%s/%s"%(i[0],i[1]) for i in list]
# print list2

# x=Decimal('0.998531571219').quantize(Decimal('0.00'))
# a= 0.998531571219
# value = round(a, 3)
# print x,type(x),value
# proxys=[]
# proxy=[123,1234]
# proxys.append(proxy)
#
# proxy=[123,1234]
# proxys.append(proxy)
#
# print proxys
# l = [{'ip':'123.1.1.1','port':80},{'ip':'123.1.1.1','port':80},{'ip':'123.1.2.1','port':80},{'ip':'123.1.1.1','port':81}]
#
# # for d in l:
# #    print  [tuple(d.items())]
# print [tuple(d.items()) for d in l]
#
# print [dict(t) for t in set([tuple(d.items()) for d in l])]
import requests

r = requests.get('http://127.0.0.1:8000/delete?ip=120.92.3.127')
print
r.text