# -*- coding: utf-8 -*-
import scrapy
import time,re

class XinSpider(scrapy.Spider):
    name = 'xin'
    allowed_domains = []
    start_urls = ['https://tech.sina.com.cn/']
    cookies={'vjlast': '1541129407', 'SINAGLOBAL': '114.249.232.244_1541129408.485601', 'Apache': '172.16.7.96_1543535404.322739', 'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5Tw1EZVhNYzRhZjVc_R2zY', 'vjuids': '62cfb576c.166d2788952.0.d99dbd6227d4a', 'U_TRS1': '000000f5.4111e41.5bdbc4c0.fef9d8b3', 'UOR': ',tech.sina.com.cn,', 'lxlrttp': '1541383354', 'TUIJIAN_1': 'usrmdinst_2', 'ULV': '1543535635000:6:6:2:172.16.7.96_1543535404.322739:1543535401886', 'SUB': '_2AkMsmkoef8NxqwJRmfkXzmnra4hyyA_EieKaxrvFJRMyHRl-yD9jqnY_tRB6Bxpk8UGJfRvB2xXb6yY0pa-Z97pyKAHU', 'hqEtagMode': '1', 'reco': 'usrmdinst_6'}
    da = set()
    def parse(self, response):

        # time.sleep(2)
        t_time=str(time.time())[:-8]

        url='https://cre.mix.sina.com.cn/api/v3/get?&cateid=1z&cre=tianyi&mod=pctech&merge=3&top_id=%2CA1u1J%2CA1rkN%2CA1s5b%2CA1mJl%2CA1PbX%2CA1MSP%2CA1fbh%2CA1Rzi%2CA1MWO%2CA1MEd%2C%2C9Eux1%2C%2C&ctime='+t_time
        #url='https://cre.mix.sina.com.cn/api/v3/get?&cateid=1z&cre=tianyi&mod=pctech&top_id=%2CA1u1J%2CA1rkN%2CA1s5b%2CA1mJl%2CA1PbX%2CA1MSP%2CA1fbh%2CA1Rzi%2CA1MWO%2CA1MEd%2C%2C9Eux1%2C%2C&ctime=1543456689'
        #print(url)
        yield scrapy.Request(url,callback=self.parse1,cookies=self.cookies)
    def parse1(self,response):
            title=re.findall('"title":"(.*?)"',response.text,re.S)
            #print(len(title))
            urls=re.findall('"url":"(.*?)"',response.text,re.S)

            ctime=str(re.findall('"ctime":(\d{10})',response.text,re.S)[-1])

            print(ctime)
            href='https://cre.mix.sina.com.cn/api/v3/get?&cateid=1z&cre=tianyi&mod=pctech&merge=3&top_id=%2CA1u1J%2CA1rkN%2CA1s5b%2CA1mJl%2CA1PbX%2CA1MSP%2CA1fbh%2CA1Rzi%2CA1MWO%2CA1MEd%2C%2C9Eux1%2C%2C&ctime='+ctime
            yield scrapy.Request(href,callback=self.parse1)

            for url in urls:
                #print(title,url)
                yield scrapy.Request(url,callback=self.parse2)
    def parse2(self,response):
        url=response.url
        self.da.add(url)
        #print('=================================')
        #print(len(self.da))
        try:
            title=response.xpath("//h1[@class='main-title']/text()").extract()
            if title==[]:
                raise Exception('Title is none')
            else:
                title=title[0]
                print(title)

        except Exception as e:
            print('舍去')

        try:
            shijian=response.xpath("//span[@class='date']/text()").extract()
            if shijian==[]:
                raise Exception('shijan is none')
            else:
                shijian=shijian[0]
        except Exception as e:
            print('舍去')

        laiyuan=response.xpath("//span[@class='source']/a[@class='source ent-source']/text()").extract()
        if laiyuan==[]:
            laiyuan='kong'
        else:
            laiyuan=laiyuan[0]
        daodu=response.xpath("//meta[@name='description']/@content/text()").extract()
        if daodu==[]:
            daodu='kong'
        else:
            daodu=daodu[0]
        keywords=response.xpath("//meta[@name='keywords']/@content/text()").extract()
        if keywords==[]:
            keywords='kong'
        else:
            lkeywords=keywords[0]
        imgurl=response.xpath("//div[@class='img_wrapper']//img/@src").extract()
        if imgurl==[]:
            imgurl='kong'
        else:
            imgurl=imgurl[0]
        neirong=response.xpath("//div[@id='artibody']/p/text()").extract()
        if neirong==[]:
            neirong='kong'
        else:
            neirong='_'.join(neirong)
        print(title,shijian,laiyuan,keywords,imgurl,daodu,neirong)

