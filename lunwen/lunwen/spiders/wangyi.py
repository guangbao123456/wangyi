# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import os,datetime
import io,sys
import re,json
from ..items import LunwenItem
class WnagYi(CrawlSpider):
    name = 'wangyi'
    #allowed_domains = []
    #start_urls = ['http://tech.163.com/']
    start_urls = ['http://tech.163.com/gd/']
    rules = (
        #http://tech.163.com/special/00097UHL/tech_datalist_02.js?callback=data_callback
        Rule(LinkExtractor(allow=r'http://tech.163.com/special/gd2016_0\d/'),follow=True),
        #[a - zA - Z0 - 9]
        Rule(LinkExtractor(allow=r'http://tech.163.com/18/\d{4}/\d{2}/\w{16}.html',restrict_css="h3.bigsize a"),callback='parse_item'),
    )
    def parse_item(self, response):
        #sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
        s=Selector(text=response.text)
        item=LunwenItem()
        arturl = response.url
        item['arturl']=arturl
        t=datetime.datetime.now()
        shijian = s.xpath("//div[@class='post_time_source']/text()").extract()

        if len(shijian) == 0:
            raise Exception('shijian is none')
        else:
            shijian = shijian[0].strip()[:-4]

        try:
            title=s.xpath("//div/h1/text()").extract()
            if len(title)==0:
                raise Exception('title is none')
            else:

                item['title'] = title[0]
        except Exception as e:
            if not os.path.exists('log'):
                os.mkdir('log')
            with open('log/' + 'log3.txt', 'a+', encoding='utf-8')as f:
                f.write('{},\t{}'.format(t, arturl) + '\n')
        laiyuan=s.xpath("//span[@class='left']/text()").extract()
        if len(laiyuan) == 0:
            laiyuan='无'
        else:
            laiyuan=laiyuan[0]
        author=s.xpath("//span[@class='ep-editor']/text()").extract()
        if author==[]:
            author='kong'
        else:
            author=author[0]
        zhengwen=s.xpath("//div[@id='endText']/p/text()").extract()
        if len(zhengwen)==0:
            zhengwen='kong'
        else:
            zhengwen='_'.join(zhengwen).strip()
        tuurl=s.xpath("//div[@id='endText']/p/img/@src").extract()
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
