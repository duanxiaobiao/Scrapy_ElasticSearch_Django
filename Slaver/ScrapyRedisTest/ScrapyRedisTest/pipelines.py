# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

import pymysql
from redis import Redis
from scrapy.exceptions import DropItem

from ScrapyRedisTest.bloomFilter import BloomFilter
from ScrapyRedisTest.es_operation import ArticleType
from ScrapyRedisTest.function import gen_suggests


redis = Redis('localhost', 6379, 0)

class ScrapyredistestPipeline(object):


    def process_item(self, item, spider):
        url = item["article_link"]
        bf = BloomFilter()
        if bf.isContains(url.encode('utf-8')):  # 判断字符串是否存在
            print('exists!')
            raise DropItem('{} ==========> 已存在,抛弃掉.'.format(item))
        else:
            print('not exists!')
            bf.insert(url.encode('utf-8'))
            print('===============items_finger指纹不存在该指纹,已插入,并返回item,由ElasticSearch保存.')
            return item







class MySQLPipeline(object):

    def __init__(self):
        self.connect =  pymysql.connect(
            host='localhost',
            # mysql数据库的端口号
            port=3306,
            # 数据库的用户名
            user='root',
            # 本地数据库密码
            passwd='root',
            # 表名
            db='csdn',
            # 编码格式
            charset='utf8'
        )
        # 2. 创建一个游标cursor, 是用来操作表。
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print(item)
        # 3. 将Item数据放入数据库，默认是同步写入。
        self.cursor.execute('insert into csdn(article_type,nick_name,article_title,article_link,article_desc,comments,digg,user_name,views,source)'
                            ' VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(
                                item["article_type"],item["nick_name"],item["article_title"],item["article_link"],item["article_desc"],
                                item["comments"], item["digg"], item["user_name"], item["views"],item["source"]
                        ))
        self.connect.commit()
        return item

    # 关闭数据库
    def close_spider(self, spider):
        print("数据库关闭.")
        self.cursor.close()
        self.connect.close()
        pass




class ElasticsearchPipeline(object):


    def process_item(self,item,spider):
        article = ArticleType()
        article.article_type = item["article_type"]                 # 文章类型
        article.nick_name = item["nick_name"]                       # 昵称
        article.article_title = item["article_title"]               # 文章标题
        article.article_link = item["article_link"]                 # 文章链接
        article.article_desc = item["article_desc"]                 # 文章描述
        article.comments = item["comments"]                         # 文章评论
        article.digg = item["digg"]                                 # 文章点赞数
        article.user_name = item["user_name"]                       # user用户名
        article.views = item["views"]                               # 观看数
        article.source = item["source"]                             # 来源
        # =============================================================================
        article.article_img = item["article_img"]   # 文章中的图片
        article.user_url = item["user_url"]   # 用户博客主页的URL
        article.user_img = item["user_img"]  # 用户头像的url
        # if article.article_link in self.urls_seen:
        #     raise DropItem("Duplicate item found: %s" % article.article_title)
        # else:


        article.suggest = gen_suggests(ArticleType._doc_type.index,((article.article_title,10),(article.article_desc,7)))
        article.save()
        print("=====================ElasticSearch管道保存成功!======================")
        return item
