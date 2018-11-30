# -*- coding: utf-8 -*-
import scrapy
import io,sys,time
import re
class DongSpider(scrapy.Spider):
    name = 'dong'
    allowed_domains = []
    start_urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&pvid=d74d569c033a409d92b02ea481435d0e']
    headers={'user-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    def parse(self, response):
        sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
        #print(response.text)
        #前30个数据静态的可以直接xpath抓取
        all=response.xpath("//ul[@class='gl-warp clearfix']/li/div")
        for a in all:
            title=a.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()").extract()[0]
            price=a.xpath("./div[@class='p-price']/strong/i/text()").extract()[0]

            print(price)
        print(len(all))
        #后面30个的数据找接口，需要获取时间戳
        t=time.time()
        #时间戳需保留5位小数
        tt='%.5f'%t
        url='https://search.jd.com/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page=2&s=28&scrolling=y&log_id='+str(tt)+'&tpl=3_M'#&show_items=100001172674,5089273,7694047,7437788,7357933,5089235,7081550,8024543,100000349372,6946605,7049459,5089225,6733024,7643003,7283905,8240587,7299782,8058010,7293056,8261721,7437786,5821455,8735304,100000651175,7437564,100000177756,6600258,8033419,100000287145,7651927'
        yield scrapy.Request(url,callback=self.parse1,headers=self.headers)
    def parse1(self,response):
        all = response.xpath("//li[@class='gl-item']/div")
        for b in all:
            title = b.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()").extract()[0]
            href ='https:'+ b.xpath(".//div[@class='p-name p-name-type-2']/a/@href").extract()[0]
            price = b.xpath("./div[@class='p-price']/strong/i/text()").extract()[0]

            print(title,href)
            yield scrapy.Request(href,callback=self.parse2)
    def parse2(self,response):
        #详情页
        print(response.url)
        key=re.findall('com/(.*?)\.html',response.url)[0]
        shop=response.xpath("//div[@class='popbox-inner']/div[@class='mt']/h3/a/text()").extract()[0]
        print(shop)
        #yield