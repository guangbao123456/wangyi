# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import os,datetime
from scrapy import log
from ..items import LunwenItem
#class LunSpider(scrapy.Spider):
class LunSpider(CrawlSpider):
    name = 'lun'
    #allowed_domains = ['lun.com']
    #start_urls = ['https://blog.csdn.net/']
    start_urls = ['http://www.81uav.cn/uav-news/5.html']
    #http://www.81uav.cn/uav-news/201811/28/45858.html
    rules = (
        #Rule(LinkExtractor(allow=(r'http://www.81uav.cn/uav-news/5_[0-9].html',)), callback='parse_item1',follow=True),
        Rule(LinkExtractor(allow=(r'http://www.81uav.cn/uav-news/\d{6}/\d{2}/\d+.html',)),callback='parse_item'),
    )
    def parse_item(self, response):
        s=Selector(text=response.text)
        item=LunwenItem()
        arturl = response.url
        item['arturl']=arturl
        t=datetime.datetime.now()
        try:
            title=s.css('div.news_left h1::text').extract()
            if len(title)==0:
                raise Exception('title is none')
            else:
                title=title[0]
                item['title'] = title
        except Exception as e:

            if not os.path.exists('log'):
                os.mkdir('log')
            with open('log/' + 'log1.txt', 'a+', encoding='utf-8')as f:
                f.write('{},\t{}'.format(t, arturl) + '\n')

        xinxi = s.css('div.info ::text').extract()[-4].replace('\xa0', '')
        shijian = re.findall('发布日期：(.*?)来源', xinxi, re.S)
        if len(shijian)==0:
            log.msg('This is a error %s' % arturl, level=log.WARNING)
            raise Exception('shijian is none')

        else:
            shijian=shijian[0]

        laiyuan=re.findall('来源：(.*)',xinxi,re.S)
        if len(laiyuan) == 0:
            laiyuan='weizhi'
        else:
            a=laiyuan[0].find('作者')
            laiyuan=laiyuan[0][0:a]

        author=re.findall('作者：(.*)',xinxi,re.S)
        if len(author)==0:
            author='kong'
        else:
            author=author[0]
        zhengwen=s.css('div.content p::text').extract()
        if len(zhengwen)==0:
            zhengwen='kong'
        else:
            zhengwen=zhengwen[0]
        tuurl=s.css('div#content p img::attr(src)').extract()
        if len(tuurl)==0:
            tuurl='空'
        else:
            tuurl=','.join(tuurl)
        daodu=s.xpath('//meta[@name="description"]/@content').extract()
        if len(daodu)==0:
            daodu='kong'
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
