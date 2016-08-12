# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from hot.items import HotItem
import json
import sys
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

class bdSpider(scrapy.Spider):
    name = 'baiduSpider'
    allowed_domains = ['baidu.com']

    start_urls = ['http://top.baidu.com/buzz?b=1&fr=topindex','http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1', 
                'http://top.baidu.com/buzz?b=42&c=513&fr=topbuzz_b341_c513', 'http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513', 
                'http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513', 'http://top.baidu.com/buzz?b=11&c=513&fr=topbuzz_b344_c513']
    def parse(self, response):
        print('##### start parse')

        item = HotItem()
        item['src']='baidu'

        now = datetime.datetime.now()
        dateidxstr = str(now.year) + '-' + str(now.month) + '-' + str(now.day) ;
        item['dateidx'] = dateidxstr

        if response.url == 'http://top.baidu.com/buzz?b=1&fr=topindex':
            item['cate'] = "realtime"
        elif response.url == 'http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b1':
            item['cate'] = "hot"
        elif response.url == 'http://top.baidu.com/buzz?b=42&c=513&fr=topbuzz_b341_c513':
            item['cate'] = "7days"
        elif response.url == 'http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b42_c513':
            item['cate'] = "social"
        elif response.url == 'http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513':
            item['cate'] = "entertainment"
        elif response.url == 'http://top.baidu.com/buzz?b=11&c=513&fr=topbuzz_b344_c513':
            item['cate'] = "sports"
            pass

        for detail in response.xpath('//a[@class="list-title"]'):
                    
            # get itemurl
            itemurl = detail.xpath('@href').extract_first()
            item['url']=itemurl

            # get content
            itemcontent = detail.xpath('text()').extract_first()
            item['key']=itemcontent.encode('utf-8')

            yield item




    
