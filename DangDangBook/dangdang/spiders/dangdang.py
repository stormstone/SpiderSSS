# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider
from dangdang.items import DangdangItem
from datetime import datetime


class Dangdangspider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'dangdang'
    redis_key = 'dangdang:start_urls'
    allowed_domains = ['book.dangdang.com', 'product.dangdang.com', 'www.dangdang.com']

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        self.number = 0
        super(Dangdangspider, self).__init__(*args, **kwargs)

    def parse(self, response):
        item = DangdangItem()
        item["name"] = response.xpath("//h1/@title").extract_first()
        item["author"] = response.xpath("//span[@id='author']/a[1]/text()").extract_first()
        item["price"] = response.xpath("//p[@id='dd-price']/text()[2]").extract_first()
        item["ISBN"] = response.xpath("//div[@id='detail_describe']/ul/li[5]/text()").extract_first()
        item["crawl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.number = self.number + 1
        item["id"] = self.number
        yield item
