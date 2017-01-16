# coding:utf-8
import base64
import re

str = '''
<script type="text/javascript">Proxy('NzcuODcuMjEuODY6ODA4MA==')</script></li>
'''
match = re.search('Proxy\(.+\)', str)
print
match.group()
ip_port = base64.b64decode(match.group().replace("Proxy('", "").replace("')", ""))
print
ip_port
