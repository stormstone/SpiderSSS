# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def remove_space(value):
    return value.strip()


class DangdangItem(scrapy.Item):
    collection = 'dangdang'
    name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(remove_space))
    crawl_time = scrapy.Field()
    ISBN = scrapy.Field()
    id = scrapy.Field()


class MasterRedisItem(scrapy.Item):
    url = scrapy.Field()
