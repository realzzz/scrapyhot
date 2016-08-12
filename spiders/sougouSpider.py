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

class hsSpider(scrapy.Spider):
    name = 'sougouSpider'
    allowed_domains = ['sougou.com']

    start_urls = ['http://top.sogou.com/']
    def parse(self, response):
        print('##### start parse')

        now = datetime.datetime.now()
        dateidxstr = str(now.year) + '-' + str(now.month) + '-' + str(now.day); 

        hots = response.xpath('//div[@class="m_con_1 fl"]')

        for hotitem in hots.xpath('.//td[@class="any_tit"]/span/a'):
            item = HotItem() 

            item['dateidx'] = dateidxstr     
            item['cate'] = 'hot';
            item['src'] = 'sougou';
            # get itemurl
            itemurl = hotitem.xpath('@href').extract_first()
            item['url']=itemurl

            # get content
            itemcontent = hotitem.xpath('text()').extract_first()
            item['key']=itemcontent.encode('utf-8')
            yield item

        weeks = response.xpath('//div[@class="m_con_2 fl"]')

        for weekitem in weeks.xpath('.//td[@class="any_tit"]/span/a'):
            item = HotItem() 

            item['dateidx'] = dateidxstr     
            item['cate'] = '7days';
            item['src'] = 'sougou';
            # get itemurl
            itemurl = weekitem.xpath('@href').extract_first()
            item['url']=itemurl

            # get content
            itemcontent = weekitem.xpath('text()').extract_first()
            item['key']=itemcontent.encode('utf-8')
            yield item





    
