# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
class ZhiNeng(CrawlSpider):
    name='ai'
    #allowed_domains=[]
    #start_urls=['http://www.ailab.cn/']
    # rules=(
    #
    #     Rule(LinkExtractor(allow='http://www.ailab.cn/?page=\d'),follow=True),
    #     Rule(LinkExtractor(allow='http://www.ailab.cn/.*/\d+.html',restrict_css='ul.list_jc a'),callback='parse_item',),
    # )
    default=True
    def start_requests(self):
        for i in range(1,5):
            url='http://www.ailab.cn/?page='+str(i)
            yield scrapy.Request(url)

    def parse(self,response):
        if self.default:

            self.default=False
            yield scrapy.Request(url=response.url,callback=self.parse)
        else:

            s=Selector(text=response.text)
            threfs=s.css('ul.list_jc a::attr(href)').extract()
            for href in threfs:
                yield scrapy.Request(href,callback=self.parse1)
    def parse1(self,response):
        s = Selector(text=response.text)
        url=response.url
        title=s.xpath("//div[@class='box']/h1[@class='h1']/text()").extract()
        keywords=s.xpath("//meta[@name='keywords']/@content").extract()
        print(keywords)