#coding:utf-8
'''
定义规则 urls:url列表
         type：解析方式,取值 regular(正则表达式),xpath(xpath解析),module(自定义第三方模块解析)
         patten：可以是正则表达式,可以是xpath语句不过要和上面的相对应
'''
import random

'''
ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https),country(国家),area(省市),updatetime(更新时间)
 speed(连接速度)
'''
parserList = [
        {
            'urls': ['http://www.66ip.cn/%s.html'% n for n in ['index']+range(2,12)],
            'type':'xpath',
            'pattern': ".//*[@id='main']/div/div[1]/table/tr[position()>1]",
            'postion':{'ip':'./td[1]','port':'./td[2]','type':'./td[4]','protocol':''}
        },
        {
            'urls': ['http://www.66ip.cn/areaindex_%s/%s.html'%(m,n) for m in range(1,35) for n in range(1,10)],
            'type':'xpath',
            'pattern': ".//*[@id='footer']/div/table/tr[position()>1]",
            'postion':{'ip':'./td[1]','port':'./td[2]','type':'./td[4]','protocol':''}
        },
        {
            'urls': ['http://www.kuaidaili.com/proxylist/%s/'% n for n in range(1,11)],
            'type': 'xpath',
            'pattern': ".//*[@id='index_free_list']/table/tbody/tr[position()>0]",
            'postion':{'ip':'./td[1]','port':'./td[2]','type':'./td[3]','protocol':'./td[4]'}
        },
        {
            'urls': ['http://www.kuaidaili.com/free/%s/%s/'% (m,n) for m in ['inha', 'intr', 'outha', 'outtr'] for n in range(1,11)],
            'type':'xpath',
            'pattern': ".//*[@id='list']/table/tbody/tr[position()>0]",
            'postion':{'ip':'./td[1]','port':'./td[2]','type':'./td[3]','protocol':'./td[4]'}
        },
        {
            'urls': ['http://www.cz88.net/proxy/%s'% m for m in ['index.shtml']+['http_%s.shtml' % n for n in range(2, 11)]],
            'type':'xpath',
            'pattern':".//*[@id='boxright']/div/ul/li[position()>1]",
            'postion':{'ip':'./div[1]','port':'./div[2]','type':'./div[3]','protocol':''}

        },
        {
            'urls': ['http://www.ip181.com/daili/%s.html'% n for n in range(1, 11)],
            'type':'xpath',
            'pattern': "html/body/div[2]/div/div[2]/div/div[3]/table/tbody/tr[position()>1]",
            'postion':{'ip':'./td[1]','port':'./td[2]','type':'./td[3]','protocol':'./td[4]'}

        },
        {
            'urls': ['http://www.xicidaili.com/%s/%s'%(m,n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 8) ],
            'type':'xpath',
            'pattern': ".//*[@id='ip_list']/tr[position()>1]",
            'postion':{'ip':'./td[2]','port':'./td[3]','type':'./td[5]','protocol':'./td[6]'}
        }

        ]
'''
数据库的配置
'''
DB_CONFIG={
    'dbType':'sqlite',#sqlite,mysql,mongodb
    'dbPath':'./data/proxy.db',#这个仅仅对sqlite有效
    'dbUser':'',#用户名
    'dbPass':'',#密码
    'dbName':''#数据库名称

}

CHINA_AREA=[u'河北',u'山东',u'辽宁',u'黑龙江',u'吉林'
    ,u'甘肃',u'青海',u'河南',u'江苏',u'湖北',u'湖南',
            u'江西',u'浙江',u'广东',u'云南',u'福建',
            u'台湾',u'海南',u'山西',u'四川',u'陕西',
            u'贵州',u'安徽',u'重庆',u'北京',u'上海',u'天津',u'广西',u'内蒙',u'西藏',u'新疆',u'宁夏',u'香港',u'澳门']
QQWRY_PATH="./data/qqwry.dat"

THREADNUM = 20
API_PORT=8000
'''
爬虫爬取和检测ip的设置条件
不需要检测ip是否已经存在，因为会定时清理
'''
UPDATE_TIME=30*60#每半个小时检测一次是否有代理ip失效
MINNUM = 200 #当有效的ip值小于一个时 需要启动爬虫进行爬取
MAXTIME = 24*60 #当爬取存储开始一直使用的最大时间，如果超过这个时间，都删除

TIMEOUT = 5#socket延时



'''
反爬虫的设置
'''
'''
重试次数
'''
RETRY_TIME=3


'''
USER_AGENTS 随机头信息
'''
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

HEADER = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}

TEST_URL='http://www.ip138.com/'