import scrapy
from scrapy import Selector, Request
from urllib import parse
from dangdang.items import MasterRedisItem


class HouseSpider(scrapy.Spider):
    name = 'dangmaster'
    allowed_domains = ['category.dangdang.com', 'book.dangdang.com']
    start_urls = ['http://book.dangdang.com/01.03.htm?ref=book-01-A']

    def parse(self, response):
        url_nodes = response.xpath("//div[@class='con flq_body']/div[@class='level_one ']/dl/dt/a/@href").extract()
        for url_node in url_nodes:
            yield Request(url=parse.urljoin(response.url, url_node), callback=self.parse_list)

    def parse_list(self, response):
        next_url = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse_list)
        url_nodes = response.xpath("//div[@class='con shoplist']/div/ul/li/a/@href").extract()
        for url_node in url_nodes:
            item = MasterRedisItem()
            item['url'] = url_node
            yield item
