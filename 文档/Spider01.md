# Python网络爬虫

### 网络爬虫简介：

爬虫：**请求**网站并**提取**数据的**自动化**程序。

通过爬虫获取数据，是大数据数据来源的一个重要方式。

爬虫场景：

- 最基本HTML页面的爬取：只需请求页面url得到页面的HTML源码，通过解析页面得到数据。
- Ajax数据爬取：现在许多网页出于对页面效果的考虑，使用Ajax异步加载数据。这样的网页可以分析页面的Ajax请求，得到请求url和参数模拟进行数据获取。
- 动态渲染页面爬取：有些页面是不能在网页看到真正的HTML，这些HTML可能是通过JavaScript渲染的。爬虫可以通过模拟浏览器登录来进行获取。
- 模拟登录：有些网站必须通过登录才能获取数据，爬虫就必须模拟登录后才有可能得到想要的数据。
- 代理的使用：很多网站都有反爬措施，一个ip大量获取数据可能会被封，需要使用大量代理ip进行隐藏。
- APP的爬取：移动端的信息只能在手机上看到，爬虫必须模拟手机的操作或者破解数据请求方式才有可能获取相应数据。



## 一、网页端爬虫

### 1.环境安装

#### 1.1 python环境

通过Anaconda安装python环境，Anaconda是Python的包管理器和环境管理器，附带了一大批常用数据科学包。

Anaconda下载地址：https://repo.anaconda.com/archive/ ，找到对应系统版本下载，推荐使用python3.6版本。

参考安装教程：https://blog.csdn.net/ITLearnHall/article/details/81708148

#### 1.2 Selenium安装

Selenium是一个浏览器自动化测试框架，Selenium测试直接运行在浏览器中，就像真正的用户在操作一样。框架底层使用JavaScript模拟真实用户对浏览器进行操作。对于爬虫来说，有些页面是通过Ajax动态获取数据的，所以可以通过selenium加载动态页面，以便获取页面数据。

使用selenium需要下载对应浏览器版本的驱动，对于chrome浏览器，需要下载chromedriver。

chromedriver下载地址（主要浏览器版本）：http://npm.taobao.org/mirrors/chromedriver/

下载完成后需要将chromedriver.exe配置到环境变量，可以直接将chromedriver.exe放到anaconda安装目录，因为anaconda环境变量如果是配置好的，把chromedriver.exe放在路径下便能找到。

#### 1.3 python相关包

网页请求获取：urllib,requests

js渲染：selenium（chromedriver），phantomjs（命令行JavaScript）

解析页面：re（正则），lxml，beautifulsoup4，puquery（jquery解析库）

数据库：pymysql，pymongo，redis（分布式，爬取队列）

web：flask，django

#### 1.4 数据库安装MySQL、MongoDB、Redis

略

#### 1.5注意

pip版本如果不是最新，通过pip升级pip出错，则通过下载pip源码进行安装。下载地址：https://pypi.org/project/pip/#files

解压后通过命令：`python setup.py install`进行安装。



### 2.基本库的使用

#### 2.1 爬虫基本原理

在浏览网页的过程中，输入网址之后，经过DNS服务器，找到服务器主机，向服务器发出一个请求，服务器经过解析之后，发送给用户的浏览器 HTML、JS、CSS 等文件，浏览器解析出来，用户便可以看到形形色色的网页了。因此，用户看到的网页实质是由 HTML 代码构成的，爬虫爬来的便是这些内容，通过分析和过滤这些 HTML 代码，实现对图片、文字等资源的获取。

**URL**，即统一资源定位符，也就是我们说的网址，统一资源定位符是对可以从互联网上得到的资源的位置和访问方法的一种简洁的表示，是互联网上标准资源的地址。互联网上的每个文件都有一个唯一的URL，它包含的信息指出文件的位置以及浏览器应该怎么处理它。

> URL的格式由三部分组成：
> ①第一部分是协议(或称为服务方式)。
> ②第二部分是存有该资源的主机IP地址(有时也包括端口号)。
> ③第三部分是主机资源的具体地址，如目录和文件名等。

爬虫爬取数据时必须要有一个目标的URL才可以获取数据，因此，它是爬虫获取数据的基本依据，准确理解它的含义对爬虫学习有很大帮助。

#### 2.2 Urllib库基本使用

Urllib是一个python内置的HTTP请求库。

##### 2.2.1 基本方法：

```python
# url:  需要打开的网址
# data：Post提交的数据
# timeout：设置网站的访问超时时间
urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)
```

直接用urllib.request模块的urlopen()获取页面，page的数据格式为bytes类型，需要decode()解码，转换成str类型。

```python
import urllib
response = urllib.request.urlopen("http://www.baidu.com")
page = response.read()
page = page.decode('utf-8')
```

**urlopen返回对象提供方法：**

- read() , readline() ,readlines() , fileno() , close() ：对HTTPResponse类型数据进行操作
- info()：返回HTTPMessage对象，表示远程服务器返回的头信息
- getcode()：返回Http状态码。如果是http请求，200请求成功完成;404网址未找到
- geturl()：返回请求的url

##### 2.2.2 使用Request
```python
urllib.request.Request(url, data=None, headers={}, method=None)
```

使用request（）来包装请求，再通过urlopen（）获取页面。

```python
from urllib import request
url = r'http://www.lagou.com/zhaopin/Python/?labelWords=label'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}
req = request.Request(url, headers=headers)
page = request.urlopen(req).read()
page = page.decode('utf-8')
```

**用来包装头部的数据：**

- User-Agent ：这个头部可以携带如下几条信息：浏览器名和版本号、操作系统名和版本号、默认语言
- Referer：可以用来防止盗链，有一些网站图片显示来源http://***.com，就是检查Referer来鉴定的
- Connection：表示连接状态，记录Session的状态。

##### 2.2.3 Post请求
urlopen()的data参数默认为None，当data参数不为空的时候，urlopen()提交方式为Post。

```python
url = 'http://httpbin.org/post'
data = {
    'first': 'true',
    'pn': 1,
    'kd': 'Python'
}
data = parse.urlencode(data).encode('utf-8')
req = request.Request(url, data=data)
page = request.urlopen(req).read()
page = page.decode('utf-8')
```

urlencode()主要作用就是将url附上要提交的数据。 Post的数据必须是bytes或者iterable of bytes，不能是str，因此需要进行encode()编码。

##### 2.2.4 使用代理

```python
urllib.request.ProxyHandler(proxies=None)
```

当需要抓取的网站设置了访问限制，这时就需要用到代理来抓取数据。

```python
data = {
    'first': 'true',
    'pn': 1,
    'kd': 'Python'
}
proxy = request.ProxyHandler({'http': 'ip:port'})  # 设置proxy
opener = request.build_opener(proxy)  # 挂载opener
request.install_opener(opener)  # 安装opener
data = parse.urlencode(data).encode('utf-8')
page = opener.open(url, data).read()
page = page.decode('utf-8')
print(page)
```

##### 2.2.5 小结

urllib提供的功能就是利用程序去执行各种HTTP请求。如果要模拟浏览器完成特定功能，需要把请求伪装成浏览器。伪装的方法是先监控浏览器发出的请求，再根据浏览器的请求头来伪装，`User-Agent`头就是用来标识浏览器的。



#### 2.3 Requests库基本使用

安装：`pip install requests` （anaconda已经自带）

```python
import json
import requests

# 1.get请求
payload = {'key1': 'value1', 'key2': 'value2'}
headers = {'content-type': 'application/json'}
r = requests.get("http://httpbin.org/get", params=payload, headers=headers)
print(r.text)
# 如果返回的是json数据，可以通过r.json()进行解析
print(r.json())

# 2.post请求
url = 'http://httpbin.org/post'
# 最基本的传参方法可以利用 data 这个参数。
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post(url, data=payload)
print(r.text)
# 有时候我们需要传送的信息不是表单形式的，需要我们传JSON格式的数据过去，
# 所以我们可以用json.dumps()方法把表单数据序列化。
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload))
print(r.text)
# 如果想要上传文件，那么直接用 file 参数即可
files = {'file': open('test.txt', 'rb')}
r = requests.post(url, files=files)
print(r.text)
# requests 是支持流式上传的，这允许你发送大的数据流或文件而无需先把它们读入内存。
# 要使用流式上传，仅需为你的请求体提供一个类文件对象即可
with open('massive-body') as f:
    requests.post('http://some.url/streamed', data=f)

# 3.cookies
cookies = r.cookies
# 另外可以利用 cookies 变量来向服务器发送 cookies 信息
requests.get(url, cookies=cookies)

# 4.超时配置
requests.get(url, timeout=0.001)

# 5.会话对象
s = requests.Session()
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")
print(r.text)

# 6.SSL证书验证
# https 开头的网站，Requests可以为HTTPS请求验证SSL证书，就像web浏览器一样。
# 要想检查某个主机的SSL证书，你可以使用 verify 参数
r = requests.get('https://kyfw.12306.cn/otn/', verify=True)
print(r.text)

# 7.代理
# 如果需要使用代理，你可以通过为任意请求方法提供 proxies 参数来配置单个请求
proxies = {
    "https": "http://41.118.132.69:4433"
}
r = requests.post("http://httpbin.org/post", proxies=proxies)
print(r.text)

# 注：http://httpbin.org 是一个用来测试http的网址。
```

其他更多用法参见官方文档。

Requests官方文档：http://docs.python-requests.org/zh_CN/latest/



#### 2.4 Beautiful Soup库基本使用

Beautiful Soup是一个可以从HTML或XML文件中提取数据的Python库

安装：`pip install beautifulsoup4` (anaconda已经自带)

##### 2.4.1 典型用法

```python
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# 创建 beautifulsoup 对象
soup = BeautifulSoup(html)
# 打印一下 soup 对象的内容，格式化输出
print(soup.prettify)

# 结构化数据解析
print(soup.title)  # 获取title
print(soup.title.name)  # title标签名称
print(soup.title.string)  # title标签内容
print(soup.title.parent.name)  # 父标签
print(soup.p['class'])  # 属性获取
print(soup.find_all('a'))  # 查找所有标签
print(soup.find(id="link3"))  # 通过id查找
for link in soup.find_all('a'):  # 遍历获取所有a标签
    print(link.get('href'))  # 获取a标签href属性

```

##### 2.4.2 对象的种类

Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:

- Tag：`Tag` 对象与XML或HTML原生文档中的tag相同（就是 HTML 中的一个个标签）。
  - Name：每个tag都有自己的名字
  - Attributes：一个tag可能有很多个属性
- NavigableString：可以遍历的字符串。得到了标签的内容，要想获取标签内部的文字，用 .string 即可。
- BeautifulSoup：`BeautifulSoup` 对象表示的是一个文档的全部内容.大部分时候,可以把它当作 `Tag` 对象,它支持 [遍历文档树](https://beautifulsoup.readthedocs.io/zh_CN/latest/#id18) 和 [搜索文档树](https://beautifulsoup.readthedocs.io/zh_CN/latest/#id27) 中描述的大部分的方法.
- Comment：`Comment` 对象是一个特殊类型的 `NavigableString` 对象----注释及特殊字符串。

##### 2.4.3 遍历文档树

- 直接子节点：
  - .contents：tag 的 .content 属性可以将tag的子节点以列表的方式输出
  - .children：它返回的不是一个 list，不过我们可以通过遍历获取所有子节点。
- 所有子孙节点：.descendants
- 父节点：.parent
- 全部父节点：.parents
- 兄弟节点：.next_sibling（下一个兄弟节点）  .previous_sibling（上一个兄弟节点）
- 全部兄弟节点：.next_siblings  .previous_siblings
- 前后节点：.next_element  .previous_element。并不是针对于兄弟节点，而是在所有节点，不分层次。
- 所有前后节点：.next_elements  .previous_elements 属性

##### 2.4.4 搜索文档树 find_

对于上面所有层级节点（父、子、兄弟），都有对应的find方法。搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件

​		find_*( name , attrs , recursive , text , **kwargs )

##### 2.4.5 CSS选择器 soup.select()

- 通过标签名查找：soup.select('title')、soup.select('a')

- 通过类名查找：soup.select('.sister') 

- 通过 id 名查找：soup.select('#link1')

- 组合查找：soup.select('p #link1')，多个条件通过空格分开

- 属性查找：soup.select('a[class="sister"]')



其他更多用法参见官方文档。

Beautiful Soup官方文档：https://beautifulsoup.readthedocs.io/zh_CN/latest/



#### 2.5 Xpath和lxml库基本使用

XPath 是一门在 XML 文档中查找信息的语言。XPath 可用来在 XML 文档中对元素和属性进行遍历。

节点关系：父（Parent）、子（Children）、同胞（Sibling）、先辈（Ancestor）、后代（Descendant）。

选取节点：XPath 使用路径表达式在 XML 文档中选取节点。节点是通过沿着路径或者 step 来选取的。



**七种类型的节点：元素、属性、文本、命名空间、处理指令、注释以及文档节点（或称为根节点）。**

##### 2.5.1 基本表达式

| 表达式   | 描述                                                       |
| :------- | :--------------------------------------------------------- |
| nodename | 选取此节点的所有子节点。                                   |
| /        | 从根节点选取。                                             |
| //       | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 |
| .        | 选取当前节点。                                             |
| ..       | 选取当前节点的父节点。                                     |
| @        | 选取属性。                                                 |

##### 2.5.2 谓语（Predicates）：谓语用来查找某个特定的节点或者包含某个指定的值的节点。谓语被嵌在方括号中。

|             路径表达式             |                             结果                             |
| :--------------------------------: | :----------------------------------------------------------: |
|         /bookstore/book[1]         |        选取属于 bookstore 子元素的第一个 book 元素。         |
|      /bookstore/book[last()]       |       选取属于 bookstore 子元素的最后一个 book 元素。        |
|     /bookstore/book[last()-1]      |      选取属于 bookstore 子元素的倒数第二个 book 元素。       |
|   /bookstore/book[position()<3]    |  选取最前面的两个属于 bookstore 元素的子元素的 book 元素。   |
|           //title[@lang]           |         选取所有拥有名为 lang 的属性的 title 元素。          |
|        //title[@lang=’eng’]        |  选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。  |
|    /bookstore/book[price>35.00]    | 选取 bookstore 元素的所有 book 元素，且其中的 price 元素的值须大于 35.00。 |
| /bookstore/book[price>35.00]/title | 选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于 35.00。 |

##### 2.5.3 选取未知节点:

XPath 通配符可用来选取未知的 XML 元素。

| 通配符 |         描述         |
| :----: | :------------------: |
|   *    |  匹配任何元素节点。  |
|   @*   |  匹配任何属性节点。  |
| node() | 匹配任何类型的节点。 |

##### 2.5.4 选取若干路径:

通过在路径表达式中使用“|”运算符，您可以选取若干个路径。

|            路径表达式            |                             结果                             |
| :------------------------------: | :----------------------------------------------------------: |
|   //book/title \| //book/price   |          选取 book 元素的所有 title 和 price 元素。          |
|        //title \| //price        |            选取文档中的所有 title 和 price 元素。            |
| /bookstore/book/title \| //price | 选取属于 bookstore 元素的 book 元素的所有 title 元素，以及文档中所有的 price 元素。 |

##### 2.5.6 XPath 运算符

|、+、-、*、div（除法）、=、!=、<、<=、>、>=、or、and、mod

##### 2.5.7 lxml用法

```python
from lxml import etree

text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
html = etree.HTML(text)
result = etree.tostring(html)
print(result)
# xpath
result = html.xpath('//li')
print(result)
print(len(result))
print(type(result))
print(type(result[0]))
# 获取 <li> 标签下 href 为 link1.html 的 <a> 标签
result = html.xpath('//li/a[@href="link1.html"]')
print(result)
# 获取倒数第二个元素的内容
result = html.xpath('//li[last()-1]/a')
print(result[0].text)
# 获取 class 为 item-0 的标签名
result = html.xpath('//*[@class="item-0"]')
print(result[0].tag)
```



#### 2.6 Selenium库基本使用

安装：`pip install selenium`

基本使用

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")  # 根据name查找元素
elem.send_keys("pycon")  # 输入内容
elem.send_keys(Keys.RETURN)  # 回车
print(driver.page_source)  # 返回浏览器渲染后页面
```

##### 2.6.1 页面操作









selenium官网：https://www.seleniumhq.org/docs/index.jsp

selenium-python文档：https://selenium-python.readthedocs.io/index.html



#### 2.7 PyQuery库基本使用

#### 2.8 正则表达式

暂略。



### 3.scrapy框架的使用

#### 3.1 Scrapy框架的安装

#### 3.2 Scrapy框架基本使用

#### 3.3 Scrapy命令行详解

#### 3.4 Scrapy中选择器的用法

#### 3.5 Scrapy中Spiders的用法

#### 3.6 Scrapy中Item Pipeline的用法

#### 3.7 Scrapy中Download Middleware的用法



### 4.使用scrapy-redis实现分布式爬虫

#### 4.1 scrapy-redis的安装

#### 4.2 scrapy-redis基本原理



### 5.反爬措施

#### 5.1 代理ip的使用

#### 5.2 cookies池的使用





## 二、APP端爬虫

### 1.环境安装

#### 1.1 模拟器安装

#### 1.2 SDK安装

#### 1.3 Fiddler安装

#### 1.4 Appium安装

#### 1.5 mitmproxy安装



### 2.抓包工具的使用

#### 2.1 Fiddler配置

#### 2.2 模拟器代理配置

#### 2.3 抓包分析



### 3.移动端自动化控制

#### 3.1 APK包名获取

#### 3.2 Appium使用



### 4.利用Appium和mitmproxy抓取存储数据

#### 4.1 基本原理

#### 4.2 抓取步骤



### 5.APK脱壳反编译

#### 5.1 APK脱壳

#### 5.2 APK反编译





## References

崔庆才：https://cuiqingcai.com/

廖雪峰：https://www.liaoxuefeng.com

Urllib模块的使用：https://www.cnblogs.com/Lands-ljk/p/5447127.html

Requests官方文档：http://docs.python-requests.org/zh_CN/latest/

Xpath教程：http://www.w3school.com.cn/xpath/index.asp