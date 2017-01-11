# coding:utf-8
import requests
import json

r = requests.get('http://127.0.0.1:8000/?types=0&count=5&country=中国')
ip_ports = json.loads(r.text)
print(ip_ports)
ip = ip_ports[0][0]
port = ip_ports[0][1]
proxies = {
    'http': 'http://%s:%s' % (ip, port),
    'https': 'http://%s:%s' % (ip, port)
}
r = requests.get('http://www.baidu.com', proxies=proxies)
r.encoding = 'utf-8'
print(r.text)
