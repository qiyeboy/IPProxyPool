# IPProxys
IPProxys代理池项目，提供代理ip
<br/>
详细使用方式，请看我的博客:
http://www.cnblogs.com/qiyeboy/p/5693128.html
<br/>
##项目依赖：
<br/>
###ubuntu,debian下
<br/>
安装sqlite数据库:
apt-get install sqlite sqlite3
<br/>
安装requests库:
pip install requests
<br/>
安装lxml
apt-get install python-lxml
<br/>
###windows下
<br/>
下载[sqlite]{http://www.sqlite.org/download.html},路径添加到环境变量
<br/>
安装requests库:
pip install requests
<br/>
安装lxml:
pip install lxml或者下载[lxml windows版]{https://pypi.python.org/pypi/lxml/}
<br/>
我的微信公众号:
<br/>
![](qiye2.jpg)
<br/>
希望大家提供更多的代理网站，现在爬取的好用的代理ip还是太少。

<br/>
同时感谢[super1-chen](https://github.com/super1-chen)对项目的贡献。
<br/>
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
