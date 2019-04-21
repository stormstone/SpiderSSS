# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from DoubanBook.items import DoubanbookTagItem


class DoubanbookPipeline(object):
    # 数据库链接配置
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    psd = '123456'
    db = 'spiders'
    tb = 'doubanbook'

    # 处理item
    def process_item(self, item, spider):
        # 判断具体的item，当有多个item的时候好区分
        if isinstance(item, DoubanbookTagItem):
            # 链接数据库
            con = pymysql.connect(host=self.host, user=self.user, passwd=self.psd, db=self.db,
                                  charset=self.c, port=self.port)
            cue = con.cursor()
            # 尝试插入数据库，捕获异常
            try:
                cue.execute("insert ignore into " + self.tb +
                            " (tag_name, tag_count, tag_link) "
                            "values (%s,%s,%s)",
                            [item['tag_name'], item['tag_count'], item['tag_link']])
            except Exception as e:
                print('Insert error:', e)
                con.rollback()
            else:
                # 提交事务
                con.commit()
            # 关闭数据库链接
            con.close()
            return item
