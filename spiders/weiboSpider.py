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

class weiboSpider(scrapy.Spider):
    name = 'weiboSpider'
    allowed_domains = ['weibo.com']
    #,'http://s.weibo.com/top/summary?cate=total&key=all'
    start_urls = ['http://s.weibo.com/top/summary?cate=realtimehot','http://s.weibo.com/top/summary?cate=total&key=all']
    def parse(self, response):
        print('##### start parse')

        item = HotItem()

        now = datetime.datetime.now()
        dateidxstr = str(now.year) + '-' + str(now.month) + '-' + str(now.day);
        item['dateidx'] = dateidxstr

        if response.url == 'http://s.weibo.com/top/summary?cate=realtimehot':
            item['cate'] = "realtime"
        elif response.url == 'http://s.weibo.com/top/summary?cate=total&key=all':
            item['cate'] = "hot"
            pass

        item['src'] = 'weibo'

        bodystr = response.body_as_unicode();

        #print bodystr

        urltagstart = r'<p class=\"star_name\"><a href=\"';
        nametagstart =  '>';  #r'suda-data=\"key=tblog_search_list&value=list_all\">'
        loc = bodystr.find(urltagstart);
   

        while (loc != -1):
            locend =  bodystr.find(r'\"', loc + len(urltagstart));

            if locend == -1:
                loc = locend
                #print("hit locend -1")
                break

            item['url'] = bodystr[loc+ len(urltagstart):locend].replace("\\/", "/");
            # TODO add http://weibo.com
            #print '##URL###' + item['url']

            locname = bodystr.find(nametagstart, locend + 1);
            if locname == -1:
                #print("hit locname -1")
                loc = locname;
                break

            locnameend = bodystr.find(r'<\/a', locname + len(nametagstart));
            if locnameend == -1:
                #print("hit locnameend -1")
                loc = locnameend;
                break

            item['key']= bodystr[locname + len(nametagstart):locnameend];
            #print '##KEY###'  + item['key']

            yield item
            
            loc = locnameend +1
            loc = bodystr.find(urltagstart,loc);
            
            pass




    
