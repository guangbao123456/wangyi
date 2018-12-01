# -*- coding: utf-8 -*-
import scrapy
import re,json,os
import io,sys
import requests
from ..items import KugouItem
class KuSpider(scrapy.Spider):
    name = 'ku'
    #allowed_domains = ['gou.com']
    start_urls = ['https://www.kugou.com/']

    def parse(self, response):
        sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
        key=input('请输入歌手名：')
        if not os.path.exists(key):
            os.mkdir(key)
        item=KugouItem()
        item['author']=key
        #'https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord=%E5%91%A8%E6%9D%B0%E4%BC%A6'
        url='https://songsearch.kugou.com/song_search_v2?&keyword='+key+'&page=1&pagesize=30'
        yield scrapy.Request(url,callback=self.parse1,meta={'item':item})
    def parse1(self,response):
        item=response.meta['item']
        names=re.findall('"SongName":"(.*?)"',response.text,re.S)
        print(names)
        names=list(set(names))
        i=0
        for n in names:
            item['sname']=n

            print('{}:{}'.format(i,n))
            i += 1
        singid=int(input('歌曲id：'))
        key1=re.findall('"FileHash":"(.*?)"',response.text,re.S)[singid-1]
        href='https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash='+key1
        #href='http://fs.w.kugou.com/201811300918/17345c58d3873fa224ef4e41c4be1cf6/G063/M03/06/11/'+key1+'.mp3'
        yield scrapy.Request(href,callback=self.parse2,meta={'item':item})
    def parse2(self,response):

        #sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
        item = response.meta['item']
        playurl=re.findall('"play_url":"(.*?)"',response.text,re.S)[0].replace('\\','')
        # aname=re.findall('"author_name":"(.*?)"',response.text,re.S)[0].strip()
        # sname=re.findall('"song_name":"(.*?)"',response.text,re.S)[0]
        song=requests.get(playurl).content

        with open(item['author']+'/'+item['sname']+'.mp3','wb')as f:
            f.write(song)
        print("下载完成！")
        yield item
        #choice=input('选择：y.继续 n.退出 ')
        # while True:
        #     if choice=='y':
        #         yield scrapy.Request(self.start_urls[0],callback=self.parse)
        #     if choice=='n':
        #         break



