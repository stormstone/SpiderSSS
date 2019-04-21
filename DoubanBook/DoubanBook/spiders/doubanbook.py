# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from DoubanBook.items import DoubanbookTagItem


class DoubanbookSpider(scrapy.Spider):
    name = 'doubanbook'
    allowed_domains = ['book.douban.com']
    start_urls = ['http://book.douban.com']

    def parse(self, response):
        # 获得所有热门标签链接
        link_more = response.xpath('//div[@class="aside"]//span[@class="link-more"]//a/@href').extract_first()
        link_more = self.start_urls[0] + link_more
        # 请求热门标签链接，通过parse_tag方法解析
        return Request(link_more, self.parse_tag)

    # 解析豆瓣图书标签
    def parse_tag(self, response):
        # getall()获取所有标签链接，返回一个列表
        lst_tag_link = response.xpath('//table[@class="tagCol"]//td//a//@href').getall()
        lst_tag_count = response.xpath('//table[@class="tagCol"]//td//b//text()').getall()
        for tag_link, tag_count in zip(lst_tag_link, lst_tag_count):
            # 标签名称
            tag_name = tag_link.split('/')[-1]
            tag_link = self.start_urls[0] + tag_link
            # 返回item
            item = DoubanbookTagItem()
            item['tag_name'] = tag_name
            item['tag_count'] = tag_count
            item['tag_link'] = tag_link
            yield item

            # 请求每个标签链接，通过parse_pages解析分页，meta传递参数
            # meta = {'tag_name': tag_name, 'tag_count': tag_count}
            # yield Request(tag_link, self.parse_pages, meta=meta)
            break

    # 解析每个标签里的分页
    def parse_pages(self, response):
        meta = response.meta
        tag_name = meta['tag_name']
        count_pages = response.xpath('//div[@class="paginator"]//a/text()').extract()[-1]
        print(tag_name, count_pages)
