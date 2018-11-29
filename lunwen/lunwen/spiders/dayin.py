# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import os,datetime
from ..items import LunwenItem
class LunSpider(CrawlSpider):
    name = 'dayin'
    start_urls = ['http://www.dayinhu.com/news/category/%E7%A7%91%E6%8A%80%E5%89%8D%E6%B2%BF']
    rules = (
        Rule(LinkExtractor(allow=(r'http://www.dayinhu.com/news/category/%E7%A7%91%E6%8A%80%E5%89%8D%E6%B2%BF/page/\d',)),follow=True),
        Rule(LinkExtractor(allow=(r'http://www.dayinhu.com/news/\d{6}.html',)),callback='parse_item'),
    )
    def parse_item(self, response):
        s=Selector(text=response.text)
        item=LunwenItem()
        arturl = response.url
        item['arturl']=arturl
        t=datetime.datetime.now()
        try:
            title=s.xpath("//h1[@class='entry-title']/text()").extract()
            if len(title)==0:
                raise Exception('title is none')
            else:
                title=title[0]
                item['title'] = title
        except Exception as e:
            if not os.path.exists('log'):
                os.mkdir('log')
            with open('log/' + 'log2.txt', 'a+', encoding='utf-8')as f:
                f.write('{},\t{}'.format(t, arturl) + '\n')
        shijian = s.xpath("//time[@class='entry-date']/text()").extract()
        if len(shijian)==0:
            raise Exception('shijian is none')
        else:
            shijian=shijian[0]

        laiyuan=re.findall('来源：(.*?)</p>',response.text,re.S)
        if len(laiyuan) == 0:
            laiyuan='无'
        else:
            laiyuan=laiyuan[0]
        author=re.findall('作者:(.*?)</p>',response.text,re.S)
        if author==[]:
            author='暂无'
        else:
            author=author[0]
        print(author)
        zhengwen=s.xpath("//div[@class='entry-content']/p/text()").extract()
        if len(zhengwen)==0:
            zhengwen='空'
        else:
            zhengwen='_'.join(zhengwen)
        tuurl=s.xpath("//div[@class='entry-content']/p/img/@src").extract()
        if len(tuurl)==0:
            tuurl='空'
        else:
            tuurl=','.join(tuurl)
        daodu=s.xpath('//meta[@name="description"]/@content').extract()
        if len(daodu)==0:
            daodu='无'
        else:
            daodu=daodu[0]
        keywords=s.xpath('//meta[@name="keywords"]/@content').extract()
        if len(keywords)==0:
            keywords='空'
        else:
            keywords=keywords[0]
        item['shijian']=shijian
        item['source']=laiyuan
        item['author']=author
        item['keywords']=keywords
        item['desc']=daodu
        item['imgurl']=tuurl
        item['content']=zhengwen

        yield item
