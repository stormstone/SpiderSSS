# 一、网页端爬虫

## 1.库

网页请求获取：urllib,requests

js渲染：selenium（chromedriver），phantomjs（命令行JavaScript）

解析：re（正则），lxml，beautifulsoup4，puquery（jquery解析库）

数据库：pymysql，pymongo，redis（分布式，爬取队列）

web：flask，django

## 2.基本原理

爬虫：**请求**网站并**提取**数据的**自动化**程序

基本流程：

- 发起请求：HTTP Request，Headers，URL
- 获取响应内容：HTTP Response，Html、Json、二进制数据
- 解析内容：Html、正则、解析库、Json、二进制
- 保存数据：结构化数据

Request：请求方式、请求URL、请求头、请求体

Response：响应状态、响应头、响应体

能爬取的内容：网页文本、图片、视频、其他

解析方式：直接处理、Json解析、正则表达式、BeautifulSoup、PyQuery、Xpath

JavaScript： Ajax，Selenium，Splash，PyV8，Ghost.py

## 3.Urllib

python内置的HTTP请求库。

- urllib.request：请求模块

- urllib.error：异常处理模块

- urllib.parse：url解析模块

- urllib.robotparser：robots.txt解析模块

urlopen，request，response，handler（代理、cookie），异常处理，URL解析（urlparse，urlunparse，urljoin，urlencode）

## 4.Requests

基于urllib的简单易用HTTP库。

请求：GET、POST、PUT、DELETE

- 解析json：req.get("url").json()

- 获取二进制数据：reg.get().content
- header
- response
- 状态码

#### 高级操作：

- 文件上传：req.post(url,filse=file)
- 获取cookie：response.cookies 
- 会话维持：模拟登陆，req.Session()
- 证书验证：req.get(url,verify=False)    response.status_code      req.get(url,cert=('',''))
- 代理设置：req.get(url,proxies=proxies)
- 超时设置：req.get(url,timeout = 0.5)
- 认证设置：req.get(url,auth=('user','123'))
- 异常处理：

## 5.RE（正则）

- re.match(pattern, string, flags=0)

  贪婪匹配：.*

  非贪婪匹配：.*?

  匹配模式：re.match(re,content,re.S) //换行

  **尽量使用泛匹配、使用括号得到匹配目标、尽量使用非贪婪模式、有换行符就用re.S**

- re.search：扫描整个字符串并返回第一个成功的匹配。**为匹配方便，能用search就不用match**

- re.findall：搜索字符串，以列表形式返回所有能匹配的字符串。
- re.sub：替换字符串中每一个匹配的子串后返回替换后的字符串。
- re.compile：将一个正则表达式串编译成正则对象，以便于复用该匹配模式。

## 6.BeautifulSoup

soup = bs4.BeautifulSoup(html, 'lxml')

### 标签选择器

- 选择元素：soup.title    soup.head
- 获取名称：soup.title.name
- 获取属性：soup.p.attrs['name']     soup.p['name']
- 获取内容：soup.p.string
- 嵌套选择：soup.head.title.string
- 子节点和子孙节点：soup.p.contents    soup.p.children    soup.p.descendants（子孙）
- 父节点和祖先节点：soup.p.parent    soup.a.parents
- 兄弟节点：soup.a.next_siblings    soup.a.previous_siblings

### 标准选择器

- find( name , attrs , recursive , text , **kwargs ）
find返回单个元素

- find_all( name , attrs , recursive , text , **kwargs )   
  可根据标签名、属性、内容查找文档

  name：

    soup.find_all('ul')

  attrs：

    soup.find_all(attrs={'id': 'list-1'})

    soup.find_all(attrs={'name': 'elements'}

    soup.find_all(id='list-1')

  text：

    soup.find_all(text='Foo')

- find_parents() find_parent()

  find_parents()返回所有祖先节点，find_parent()返回直接父节点。

- find_next_siblings() find_next_sibling()

  find_next_siblings()返回后面所有兄弟节点，find_next_sibling()返回后面第一个兄弟节点。

- find_previous_siblings() find_previous_sibling()

  find_previous_siblings()返回前面所有兄弟节点，find_previous_sibling()返回前面第一个兄弟节点。

- find_all_next() find_next()

  find_all_next()返回节点后所有符合条件的节点, find_next()返回第一个符合条件的节点

- find_all_previous() 和 find_previous()

  find_all_previous()返回节点后所有符合条件的节点, find_previous()返回第一个符合条件的节点

### CSS选择器

通过select()直接传入CSS选择器即可完成选择

soup.select('.panel .panel-heading')

soup.select('#list-2 .element'）

## 7.PyQuery

jQuery

- 初始化：字符串、URL、文件
- CSS选择器：
- 查找元素：子元素（find）、父元素（parent）、兄弟元素（siblings）
- 遍历：.items()
- 获取信息：属性attr、文本text、HTML
- DOM操作：addClass、removeClass、attr、css、remove
- 伪类选择器：nth-child(2)

## 8.Selenium

自动化测试工具，爬虫中用来解决JavaScript渲染问题。

- 声明浏览器对象：webdriver.Chrome()
- 访问页面：b.get(url)
- 查找元素：
  - 单个元素：find_element_by_id('id')    by_css_selector    by_xpath
  - 多个元素：find_elements_
- 操作：
  - 元素交互操作：输入、点击、跳转
  - 交互动作：ActionChains（拖拽、双击）
  - 执行JavaScript：.execute_script()
- 获取元素信息：get_attribute()    .text    .id     .location     .size    .tag_name
- Frame：switch_to.frame()      switch_to.parent_frame()
- 等待：
  - 隐式等待    implicatly_wait()
  - 显示等待    等待到满足条件为止
- 前进后退：back    forward
- cookies：get_cookied
- 选项卡管理：switch_to_window     browser.window_handles
- 异常处理：

## 9.反爬

### 代理池

多站抓取，异步检测；定时筛选，持续更新；提供接口，易于提取

获取、过滤、更新、API

###  COOKIES池

自动登陆更新；定时验证筛选；提供外部接口

账号队列 ，生成器 ，COOKIES队列 ，定时检测，API

## 10.Scrapy

```shell
scrapy startproject projname
scrapy genspider spidername url
scrapy crawl spidername -o outputfile
scrapy check
scrapy fetch url
scrapy view url
scrapy shell url
scrapy parse url
scrapy bench
```



选择器：response.selector.    xpath     css

- settings：配置
- spider：爬取代码
- items：爬取内容定义
- piplines：items处理
- middlewares：process_request     process_response    process_exception

分布式：共享爬取队列

Scrapy-Redis

scrapyd：分布式部署



Fiddler：https://www.cnblogs.com/yyhh/p/5140852.html

## 11.XPath

XPath 是一门在 XML 文档中查找信息的语言。XPath 用于在 XML 文档中通过元素和属性进行导航。

**七种类型的节点：元素、属性、文本、命名空间、处理指令、注释以及文档节点（或称为根节点）。**

| 表达式   | 描述                                                       |
| :------- | :--------------------------------------------------------- |
| nodename | 选取此节点的所有子节点。                                   |
| /        | 从根节点选取。                                             |
| //       | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 |
| .        | 选取当前节点。                                             |
| ..       | 选取当前节点的父节点。                                     |
| @        | 选取属性。                                                 |



**谓语（Predicates）**：谓语用来查找某个特定的节点或者包含某个指定的值的节点。谓语被嵌在方括号中。

# 二、APP端爬虫

## 1.相关工具

工具：

- 模拟器：夜神模拟器
- 抓包工具：Fiddler、mitmproxy       **中间人技术**
- 自动化：**appium**（封装了标准selenium客户端库，自动化测试开源工具，跨平台（iOS、Android）、多语言，模拟点击、滑动、翻页等操作。）
- 多端部署：docker

## 2.mitmproxy

安装通过whl方式安装！！！

### mitmproxy：

启动：mitmproxy -p 8888

只支持Linux，windows可以用mitmdump、mitmweb。配置步骤：WLAN配置代理 ——> 打开mitm.it网址安装证书

过滤：f      view_filter=     -c 状态码      -d 域名     -m 请求方式

断点拦截：i       intercept=   

### mitmdump

与python脚本交互。

```shell
mitmdump -p 8888 -s test.py
```

## 3.Android

**adb**：与模拟器通信

- adb devices    设备列表，没有通过`adb connect 127.0.0.1:62001`添加设备。
- adb -s [device_name] shell
- push   pull   传输文件

**uiautomator**：UI测试工具       SDK/tools

uiautomatorviewer、uiautomator        升级版方便获取xpath

**appium**：

inspector

​	desired capability：配置appium会话，platformName、platformVersion、deviceName、appPackage、appActivity（aapt.exe工具：aapt.exe dump badging [apk路径]；adb获取：adb shell ---> **logcat | grep cmp=**   ---> 打开app）

```python
cap = {
    "platformName": "Android",
    "platformVersion": "7.1.2",
    "deviceName": "127.0.0.1:62025",
    "appPackage": "com.babytree.apps.pregnancy",
    "appActivity": "com.babytree.apps.pregnancy.MainActivity",
    "noReset": True,
    "resetKeyboard": True,
    "unicodeKeyboard": True  # 键盘输入中文支持
}
```

像F12一样点击界面获取xpath。通过id获取可能存在多个控件同id的情况。。。



### HTTPS：

SSL pinning：SSL证书绑定。在用户目录下.mitmproxy文件夹，`mitmproxy-ca-cert.p12`用于windows证书安装，`mitmproxy-ca-cert.cer`用于Android手机证书安装，通过adb push 把文件传入Android的sdcard通过安全添加证书。

Xposed框架、JustTruestMe组件。



### 流程：

- adb start-server

- Fiddler抓包，配置https、端口等，手机配置代理ip和端口，打开浏览器下载证书；
- 通过uiautomatorviewer获取界面控件的xpath；
- Appium运行起来控制手机操作；
- mitmdump运行请求获得的数据的处理脚本，对数据进行处理保存。



### python安装包：

- selenium：要下载对应版本的driver配置好环境变量，python安装selenium包；

- appium：pip install Appium-Python-Client



# 三、APP源码分析

## APK反编译：

https://blog.csdn.net/s13383754499/article/details/78914592

- apktool ：使用apktool反编译apk得到图片、XML配置、语言资源等文件，

```shell
java -jar apktool_2.0.1.jar d -f [PATH_APK] -o [PATH_OUT]
```

- dex2jar：使用dex2jar反编译apk得到Java源代码，将要反编译的APK后缀名改为.rar或者 .zip，并解压，得到其中的classes.dex文件（它就是java文件编译再通过dx工具打包而成的）

```shell
d2j-dex2jar classes.dex
```

- jd-gui ：源码查看，IDEA亦可

## 脱壳：

https://www.jianshu.com/p/138c9de2c987

工具：VirtualXposed（或者直接xposed）、FDex2

得到脱壳后得dex文件通过d2j-dex2jar反编译得到.class文件。

## JAD-反编译class文件：

[利用jdk自带的jad.exe实现批量反编译class文件](https://www.cnblogs.com/flydkPocketMagic/p/7048350.html)

```shell
jad -o -8 -r -d[PATH_OUT] -sjava [PATH_CLASS]
```



# 四、Scrapy-redis

https://blog.csdn.net/lm_is_dc/article/details/81057811

![scrapy-redis架构](https://img-blog.csdn.net/20180715221206313?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xtX2lzX2Rj/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)



# 五、注意

## 1.安装scrapy时报错

报错内容如下格式：


```shell
d:\work\anaconda3.5\include\pyconfig.h(222): fatal error C1083: Cannot open include file: 'basetsd.h': No such file or directory
error: command 'C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\BIN\\x86_amd64\\cl.exe' failed with exit status 2
```

这是安装**Twisted导致的这个错误的发生的**，需要从**非官方版本**下载twisted并安装：https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted

**Twisted**是用Python实现的基于事件驱动的网络引擎框架，Twisted支持许多常见的传输及应用层协议，包括TCP、UDP、SSL/TLS、HTTP、IMAP、SSH、IRC以及FTP。

## 2.APP爬取相关问题：

- 记得启动adb，`adb start-server`；
- 运行Appium中，uiautomatorviewer无法获取界面，需停止appium服务；
- 启动mitmdump要关闭fiddler，可能数据被fiddler拦截，mitm获取不到数据；
- Android端如果设置了fiddler或者mitmproxy代理，fiddler或mitmproxy必需开启，不然没有网；
- 



