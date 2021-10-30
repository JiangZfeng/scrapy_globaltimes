"""
10 1235431   1237415
根据九月的地址来推断, 一个月大约有2000条
9 1233000 1235000

8 1229000 1231000
7 1227000 1229000
6 1225000 1227000
5 1223000 1225000
4 1221000 1223000
3 1219000 1221000
2 1217000 1219000
1 1215000 1217000
"""


import scrapy
from globaltimes.items import *

class SpiderGlobaltimesSpider(scrapy.Spider):
    name = 'spider_globaltimes'
    allowed_domains = ['globaltimes.cn']
    start_urls = ['http://globaltimes.cn/']

    def parse(self, response):
        base_url = "http://www.globaltimes.cn/page/2021"
        # 循环新的url请求加入待爬队列，并调用回调函数 parse_page
        for page in range(1222700, 1224999):        #10月份的新闻   已经爬取了10月数据
            print(base_url + str(page) + '.shtml')
            yield scrapy.Request(base_url+'05/' + str(page) + '.shtml', dont_filter=True, callback=self.parse_page)





    def parse_page(self, response):
        item = {}

        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="article_title"]/text()').extract()

        item['article_level_one'] = response.xpath('//span[@class="cloumm_level_one"]/a/text()').extract()
        item['article_level_two'] = response.xpath('//span[@class="cloumm_level_two"]/a/text()').extract()
        item['pub_time'] = response.xpath('//span[@class="pub_time"]/text()').extract()
        item['content'] = response.xpath('//div[@class="article_right"]/text()').extract()[3:]
        item['abstract'] = response.xpath('//div[@class="article_right"]/text()').extract()[2]
        yield item
        pass

