# coding:utf-8
import json
import requests
import config

r = requests.get(url=config.TEST_IP, headers=config.HEADER, timeout=config.TIMEOUT)
json = json.loads(r.text)
print json['origin']
