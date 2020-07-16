# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem

class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain="https://www.qiushibaike.com"

    def parse(self, response):
        duanzidivs=response.xpath(r"//div[@class='col1 old-style-col1']/div")
        for duanzidiv in duanzidivs:
            author=duanzidiv.xpath(r".//a[2]/h2/text()").get()
            content=duanzidiv.xpath(r".//div[@class='content']/span/text()").getall()
            item=QsbkItem(author=author,content=content)
            yield item
        next_url=response.xpath(r"//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url,callback=self.parse)
