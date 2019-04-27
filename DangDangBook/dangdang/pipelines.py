# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy.conf import settings
from dangdang.items import DangdangItem, MasterRedisItem
import redis


class DangdangPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self, uri, dbname, sheetname):
        client = pymongo.MongoClient(uri)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('MONGO_URI'),
            dbname=crawler.settings.get('DBNAME'),
            sheetname=crawler.settings.get('SHEETNAME')
        )

    def process_item(self, item, spider):
        if isinstance(item, DangdangItem):
            data = dict(item)
            self.post.insert(data)
        return item


class MysqlPipeline(object):
    host = settings['MYSQL_HOST']
    user = settings['MYSQL_USER']
    psd = settings['MYSQL_PASSWORD']
    db = settings['MYSQL_DB']
    c = settings['CHARSET']
    port = settings['MYSQL_PORT']

    def process_item(self, item, spider):
        if isinstance(item, DangdangItem):
            con = pymysql.connect(host=self.host, user=self.user, passwd=self.psd, db=self.db,
                                  charset=self.c, port=self.port)
            cue = con.cursor()
            try:
                cue.execute("insert ignore into " +
                            settings['MYSQL_TABLE'] +
                            " (name, author, price, collection, crawl_time, ISBN) "
                            "values (%s,%s,%s,%s,%s,%s)",
                            [item['name'], item['author'], item['price'],
                             'dangdang', item['crawl_time'], item['ISBN']])
            except Exception as e:
                print('Insert error:', e)
                con.rollback()
            else:
                con.commit()
            con.close()
            return item


class RedisLinJiaPipeline(object):

    def __init__(self, host='localhost', port=6379,
                 db=2, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('REDIS_HOST'),
            port=crawler.settings.get('REDIS_PORT'),
            db=crawler.settings.get('REDIS_DB'),
            password=crawler.settings.get('REDIS_PASSWORD'),
        )

    def open_spider(self, spider):
        self.r = redis.Redis(host=self.host, port=self.port, password=self.password, db=self.db)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, MasterRedisItem):
            self.r.lpush('dangdang:start_urls', item['url'])
        return item
