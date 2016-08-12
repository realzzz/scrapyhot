# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb as mdb
from DBUtils.PooledDB import PooledDB
from MySQLdb.cursors import DictCursor

def processItem(self, item, spider):
    cur = self.dbconnection.cursor()
    decodekey = item['key']
    if item['src'] == 'weibo':
        decodekey = item['key'].decode('unicode_escape')
    querySql = "select count(*) cnt from hots where title = '"  + decodekey + "' and dateidx = '"  + item['dateidx']+  "'";
    #print(querySql)
    cur.execute(querySql)
    results=cur.fetchall()

    updateurlkey = 'wburl'
    targeturl = item['url']
    if item['src'] == 'baidu':
        updateurlkey = 'bdurl'
    elif item['src'] == 'sougou':
        updateurlkey = 'sgurl'
    elif item['src'] == 'weibo':
        updateurlkey = 'wburl'
        targeturl = 'http://s.weibo.com'+ item['url']

    if results[0]['cnt'] == 0:
        insertSql = "insert into hots(title, dateidx,"+updateurlkey+") values(%s, %s, %s)"
        insertparam = ( decodekey, item['dateidx'], targeturl )
        cur.execute(insertSql,insertparam)
        self.dbconnection.commit()
        pass
    else:
        updateSql = "UPDATE hots SET weight = weight + 1 , " + updateurlkey + "=%s where title = %s and dateidx = %s";
        print updateSql
        udpateparam = ( targeturl, decodekey, item['dateidx'])
        cur.execute(updateSql,udpateparam);
        self.dbconnection.commit()
        pass
    return item

class HotPipelineLocal(object):

    def __init__(self):
            self.pool = PooledDB(creator=mdb, mincached=1 , maxcached=100 ,
                              host='127.0.0.1' , port=3307 , user='root' , passwd='' ,
                              db='scrapy',use_unicode=True,charset='utf8',cursorclass=DictCursor)
            self.dbconnection = self.pool.connection()


    def process_item(self, item, spider):
        return processItem(self, item, spider);
