# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyredistestItem(scrapy.Item):

    article_type = scrapy.Field()       # 文章类型
    nick_name =scrapy. Field()          # 昵称
    article_title = scrapy.Field()      # 文章标题
    article_link = scrapy.Field()       # 文章链接
    article_desc = scrapy.Field()       # 文章描述
    comments = scrapy.Field()           # 文章评论数
    digg = scrapy.Field()               # 点赞数
    user_name =scrapy. Field()          # user名
    views = scrapy.Field()              # 观看数
    source = scrapy.Field()             # 来源



class ScrapyredistestItems(scrapy.Item):

    article_type = scrapy.Field()       # 文章类型  1
    nick_name =scrapy. Field()          # 昵称    2
    article_title = scrapy.Field()      # 文章标题  3
    article_link = scrapy.Field()       # 文章链接  4
    article_desc = scrapy.Field()       # 文章描述  5
    comments = scrapy.Field()           # 文章评论数 6
    digg = scrapy.Field()               # 点赞数   7
    user_name =scrapy. Field()          # user名     8
    views = scrapy.Field()              # 观看数··9
    source = scrapy.Field()             # 来源    10
    article_img = scrapy.Field()        # 文章中的图片    11
    user_url = scrapy.Field()            # 用户博客主页的URL   12
    user_img = scrapy.Field()           # 用户头像的url  13