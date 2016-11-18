# IPProxys
IPProxys代理池项目，提供代理ip
<br/>
详细使用方式，请看我的博客:
http://www.cnblogs.com/qiyeboy/p/5693128.html
<br/>
我的微信公众号:
<br/>
![](qiye2.jpg)
<br/>
希望大家提供更多的代理网站，现在爬取的好用的代理ip还是太少。

<br/>
同时感谢[super1-chen](https://github.com/super1-chen)对项目的贡献。
<br/>
##项目依赖
####ubuntu,debian下
<br/>
安装sqlite数据库:
apt-get install sqlite sqlite3
<br/>
安装requests库:
pip install requests
<br/>
安装lxml:
apt-get install python-lxml
<br/>
####windows下
下载[sqlite](http://www.sqlite.org/download.html),路径添加到环境变量
<br/>
安装requests库:
pip install requests
<br/>
安装lxml:
pip install lxml或者下载[lxml windows版](https://pypi.python.org/pypi/lxml/)
## 如何使用

将项目目录clone到当前文件夹

$ git clone 

切换工程目录

```
$ cd IPProxys
```

运行脚本

```
python IPProxys.py
```

## API 使用方法

#### 模式
```
GET /
```

####参数 


| Name | Type | Description |
| ----| ---- | ---- |
| types | int | 0: 高匿代理, 1 透明 |
| protocol | int | 0: http, 1 https |
| count | int | 数量 |
| country | str | 国家 |
| area | str | 国家 |



#### 例子
#####IPProxys默认端口为8000
<br/>
#####如果是在本机上测试：
1.访问http://127.0.0.1:8000/?types=0&count=5&country=中国
<br/>
这个链接的含义是获取5个ip地址在中国的高匿代理。
<br/>
2.响应为JSON格式，返回数据为：
<br/>
[{"ip": "220.160.22.115", "port": 80}, {"ip": "183.129.151.130", "port": 80}, {"ip": "59.52.243.88", "port": 80}, {"ip": "112.228.35.24", "port": 8888}, {"ip": "106.75.176.4", "port": 80}]


<br/>
-----------------------------2016-10-27----------------------------
<br/>
1.增加对代理的检测，测试是否能真正访问到网址，实现代理
<br/>
2.添加通过正则表达式和加载插件解析网页的方式
<br/>
3.又增加一个新的代理网站
<br/>

-----------------------------2016-7-20----------------------------
<br/>
修复bug ,将数据库进行压缩
<br/>
