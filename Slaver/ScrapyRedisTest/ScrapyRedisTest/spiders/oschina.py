import time

import scrapy
from redis import Redis

from ScrapyRedisTest.items import ScrapyredistestItems
from scrapy_redis.spiders import RedisSpider

redis_hash = Redis('127.0.0.1', 6379, 0)

class csdnSpider(RedisSpider):

    name = 'oschina'
    redis_key = 'oschina:start_urls'

    def __init__(self):

        self.number = []

    def parse(self, response):
        """
        分布式爬虫:Slaver端爬虫
                 注:
        :param response:
        :return:
        """
        if '/widgets/_space' in response.request.url : # 存在字符串 'space'的话意味着,该url为博主index主页的URL.
            # 如果此url 中包含字符串 'api' 和 'category',说明返回的值是json数据.回调函数为json
            yield scrapy.Request(response.request.url,callback=self.blog_home_article_list)
        else:
            yield scrapy.Request(response.request.url,callback=self.blog_home_category_list) # 博客主页分类列表.



    def blog_home_article_list(self,response):
        """博主的文章列表的url回调函数"""
        articles = response.xpath('//div[@id="mainScreen"]//div[@class="ui container"]//div//div[@class="item blog-item"]')
        for item in articles:
            article_title = ''.join(item.xpath('div[@class="content"]//a[@class="header"]/text()').extract()).replace('\n','').replace(' ','')
            article_link = item.xpath('div[@class="content"]//a[@class="header"]/@href').extract()[0]
            article_desc =''.join(item.xpath('div[@class="content"]//div[@class="description"]//p/text()').extract()).replace('\n','').replace(' ','')
            comments = ''.join( item.xpath('div[@class="content"]//div[@class="extra"]//div[@class="ui horizontal small list"]//div[@class="item"][4]//a/text()').extract() )    # 文章评论数
            digg = '0'  # 点赞数
            views = ''.join(item.xpath('div[@class="content"]//div[@class="extra"]//div[@class="ui horizontal small list"]//div[@class="item"][3]/text()').extract())  # 观看数
            article_images = item.xpath('div[@class="images"]')
            if article_images:
                article_img = article_images.xpath('a/img/@src').extract()[0]
            else:
                article_img = '无图片'
            get_nick_name_url = response.request.url.split('widgets')[0]
            meta = {"article_title":article_title,"article_link":article_link,"digg":digg,
                    "article_desc":article_desc,"comments":comments,"views":views,"article_img":article_img,"flag":0}
            yield scrapy.Request(get_nick_name_url,meta=meta,callback=self.get_nick_name)



    def blog_home_category_list(self,response):
        """博客主页分类url的回调函数"""
        articles = response.xpath('//div[@id="mainScreen"]//div[@class="ui container"]//div//div[@class="item blog-item"]')
        for article in articles:
            article_title = article.xpath('div[@class="content"]//a[@class="header"]/@title').extract()[0]
            article_link = article.xpath('div[@class="content"]//a[@class="header"]/@href').extract()[0]
            article_desc =article.xpath('div[@class="content"]//div[@class="description"]/p/text()').extract()[0]
            user_url = article.xpath('div[@class="content"]//div[@class="extra"]//div[@class="ui horizontal list"]//div[@class="item"][1]//a/@href').extract()[0]
            views = article.xpath('div[@class="content"]//div[@class="extra"]//div[@class="ui horizontal list"]//div[@class="item"][3]/text()').extract()[0]
            comments = article.xpath('div[@class="content"]//div[@class="extra"]//div[@class="ui horizontal list"]//div[@class="item"][4]/a/text()').extract()[0]
            digg = article.xpath('div[@class="content"]//div[@class="extra"]//div[@class="ui horizontal list"]//div[@class="item"][5]/text()').extract()[0]
            article_images = article.xpath('a[@class="ui small image"]')
            if article_images:
                article_img = article_images.xpath('img/@src').extract()[0]
            else:
                article_img = '无图片'

            meta = {"article_title": article_title, "article_link": article_link, "article_desc": article_desc,
                    "comments": comments, "views": views, "article_img": article_img,"digg":digg,"flag":1}
            yield scrapy.Request(user_url, meta=meta, callback=self.get_nick_name)



    def get_nick_name(self,response):

        Item = ScrapyredistestItems()
        Item["article_type"] = '博客'
        Item["source"] = '开源中国'
        Item["article_title"] = response.meta["article_title"]
        Item["article_link"]  = response.meta["article_link"]
        Item["article_desc"]  = response.meta["article_desc"]
        Item["comments"]  = response.meta["comments"]
        Item["views"]  = response.meta["views"]
        Item["article_img"]  = response.meta["article_img"]
        Item["nick_name"] =''.join(response.xpath("//div[@id='mainScreen']/div[@class='ui container']/div[@class='ui grid space-home']/div[@class='row']/div[@class='five wide computer five wide tablet sixteen wide mobile column']/div[@class='space-sidebar']/div[@class='ui basic center aligned segment sidebar-section user-info']/div[@class='ui header']/h3/text()").extract())
        user_img = response.xpath("//div[@class='ui grid space-home']/div[@class='row']/div[@class='five wide computer five wide tablet sixteen wide mobile column']/div[@class='space-sidebar']/div[@class='ui basic center aligned segment sidebar-section user-info']/div[1]/a/div/img/@src").extract()
        Item["user_url"]  = response.request.url
        Item["user_name"]  = response.request.url.rstrip('/').split('/')[-1]
        flag = response.meta["flag"]
        if int(flag) == 1:
            Item["digg"]  = response.meta["digg"]
        else:
            Item["digg"]  = '0'

        if not user_img:                    # print("用户头像不存在!")
            Item["user_img"] = ''
        else:                               # print("用户头像存在！")
            Item["user_img"]  = user_img[0]

        yield Item


