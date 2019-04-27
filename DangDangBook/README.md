# DangDangBook
爬取当当网的图书条目，使用Scrapy-Redis实现一个分布式网络爬虫。

基于scrapy-redis做的分布式爬虫，可以解决单机爬虫的瓶颈，单机每小时爬取量在3w5左右。主要做了当当网小说栏目的爬取，数据量在10w左右，想爬其他的可以在master端添加start_url

## 系统分布式架构
分布式采用主从结构设置一个Master服务器和多个Slave服务器，Master端分发下载任务，Slave部署Scrapy爬虫提取网页和解析提取数据，最后将解析的数据存储在同一个数据库中 。


## 运行
1. Master

   在项目中找到master_main.py文件，直接运行

2. Slave

   在项目中找到main.py文件，直接运行
