# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

import pymysql
from redis import Redis
from scrapy.exceptions import DropItem

from MasterRedisTest.settings import REDIS_HOST, REDIS_PORT, CNBLOGS_REDIS_KEY, CNBLOGS_REDIS_FINGER_VALUE, \
    CSDN_REDIS_FINGER_VALUE, \
    CNBLOGS_REDIS_START_URLS, CSDN_REDIS_START_URLS, OSCHINA_REDIS_KEY, OSCHINA_REDIS_FINGER_VALUE, \
    OSCHINA_REDIS_START_URLS, CSDN_REDIS_KEY

redis = Redis(REDIS_HOST, REDIS_PORT, 0)  # 如果连接远程的Redis,需要验证AUTH的，在0后添加变量：password=REDIS_PARAMS



class MasterredistestPipeline(object):

    # 处理数据
    def process_item(self, item, spider):
        url = item['url']
        REDIS_KEY,REDIS_VALUE,REDIS_START_URLS = 'error','urls_finger','start_urls'  # error:start_urls
        if 'csdn.net' in url :
            REDIS_KEY = CSDN_REDIS_KEY
            REDIS_VALUE = CSDN_REDIS_FINGER_VALUE
            REDIS_START_URLS = CSDN_REDIS_START_URLS
        if 'cnblogs.com' in url:
            REDIS_KEY = CNBLOGS_REDIS_KEY
            REDIS_VALUE = CNBLOGS_REDIS_FINGER_VALUE
            REDIS_START_URLS = CNBLOGS_REDIS_START_URLS
        if  'oschina.net'   in url:
            REDIS_KEY = OSCHINA_REDIS_KEY
            REDIS_VALUE = OSCHINA_REDIS_FINGER_VALUE
            REDIS_START_URLS = OSCHINA_REDIS_START_URLS
        url_hash = hashlib.md5(url.encode()).hexdigest()
        hash_user_url = redis.sadd('{0}:{1}'.format(REDIS_KEY,REDIS_VALUE), url_hash)  # 将标记插入redis
        if hash_user_url == 1:
            redis.lpush('{0}:{1}'.format(REDIS_KEY,REDIS_START_URLS), url)
        else:
            print(">" * 10 + "此URL数据库已存在,跳过,不予以存储." + "<" * 10,url)
            raise  DropItem(item)
        return item

class MySQLPipeline(object):

    def __init__(self):
        self.connect =  pymysql.connect(host='localhost',port=3306, user='root',passwd='root',
            db='csdn',charset='utf8'
        )
        # 2. 创建一个游标cursor, 是用来操作表。
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print(item)
        # 3. 将Item数据放入数据库，默认是同步写入。
        self.cursor.execute('insert into urls(url) VALUES ("{}")'.format(item["url"]))
        self.connect.commit()
        return item

    # 关闭数据库
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
        print("=============数据库关闭.==================")

