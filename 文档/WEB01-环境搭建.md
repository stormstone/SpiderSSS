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



#### 1.4 注意

pip版本如果不是最新，通过pip升级pip出错，则通过下载pip源码进行安装。下载地址：https://pypi.org/project/pip/#files

解压后通过命令：`python setup.py install`进行安装。