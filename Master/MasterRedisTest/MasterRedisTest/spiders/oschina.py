# -*- coding: utf-8 -*-
import scrapy

from MasterRedisTest.items import MasterredistestItem


class OschinaSpider(scrapy.Spider):
    name = 'oschina'
    # allowed_domains = ['www.oschina.net/blog']
    start_urls = ['http://www.oschina.net/blog']

    def parse(self, response):
        """开源中国首页左边栏的博客分类列表"""
        category_url_list = response.xpath('//div[@class="ui text compact vertical menu"]//a/@href').extract()
        # ['最新推荐','每日一搏','最新发表']
        blog_category_list =['recommend','daily','newest']

        for category in blog_category_list:
            for item in category_url_list:

                if '?classification' not in item:
                    url = item +'/widgets/_blog_index_{0}_list?classification=0&p=1'.format(category)
                else:
                    url = item.split('?')[0] +'/widgets/_blog_index_{0}_list?'.format(category)+item.split('?')[1]+'&p=1'
                # 将分类的各个url 抛入Item管道.
                Item = MasterredistestItem()
                Item['url'] = url
                yield Item

                # =============================================================

                yield scrapy.Request(url, callback=self.get_nickname_url)

                # =============================================================


                # 首页下一页的url.
                next_page_url = url.split('&p')[0]+'&p=2'
                yield  scrapy.Request(next_page_url,callback=self.index_next_url)

        # 本周最受欢迎博主和 推荐博主 的url列表.
        bloger_lists = response.xpath('//div[@class="ui items"]//div[@class="item"]//div[@class="content"]//a/@href').extract()
        for blog_url in bloger_lists:
            yield scrapy.Request(blog_url,callback=self.fans_list)



    def index_next_url(self,response):
        """首页下一页的循环回调函数"""
        blog_items = response.xpath('//div[@class="item blog-item"]')
        if blog_items:
            current_page_number = int(response.request.url.split('&p=')[1])

            # 将首页下一页的各个url 抛入Item管道.
            item = MasterredistestItem()
            item['url'] = response.request.url
            yield item

            # =============================================================

            yield scrapy.Request(response.request.url, callback=self.get_nickname_url)

            # =============================================================



            # 下一页url,回调函数 ===> index_next_url
            next_page_url = response.request.url.split('&p')[0]+'&p='+str(current_page_number+1)
            print("========首页下一页URL:",next_page_url)



            yield scrapy.Request(next_page_url,callback=self.index_next_url)
        else:
            pass

    def get_nickname_url(self,response):

        # print("=======该url为：",response.request.url)

        article_list = response.xpath('//div[@id="mainScreen"]//div[@class="ui container"]//div//div[@class="item blog-item"]//div[@class="extra"]//div[@class="ui horizontal list"]//div[1]//a/@href').extract()
        for item in article_list:
            nick_name_url = item
            # print("=======昵称的URL:",nick_name_url)
            yield scrapy.Request(nick_name_url,callback=self.fans_list)


    # 本周最受欢迎博主和 推荐博主 的粉丝列表.
    def fans_list(self,response):
        fan_index_url = response.request.url + '/widgets/_space_index_newest_blog?catalogId=0&q=&p=1'

        yield scrapy.Request(fan_index_url,callback=self.fan_index_next_page)

        # 本博主的粉丝数:
        fans_number =''.join(response.xpath("//div[@class='ui three tiny statistics user-statistics']/a[@class='statistic'][2]/div[@class='value']/text()").extract()).replace('\n','').replace(' ','').replace('\r','')
        # print("====sss====博主的粉丝数：",fans_number)
        if fans_number != '0':
            # print("=========如果粉丝数量不为0,爬取粉丝列表.======")
            fans_list_urls = response.request.url +'/followers'

            yield scrapy.Request(fans_list_urls,callback=self.fan_urls)

        # 本博主的关注数:
        follow_count =  response.xpath("//div[@class='ui three tiny statistics user-statistics']/a[@class='statistic'][3]/div[@class='value']/text()").extract()[0]\
            .replace('\n','').replace(' ','').replace('\r','')
        # print("====sss====博主的关注数：",follow_count)
        if follow_count != '0':
            # print("=========如果博主关注数不为0,爬取博主关注列表.======")
            blog_follow_urls = response.request.url +'/following'
            yield scrapy.Request(blog_follow_urls,callback=self.bloger_follow_list)


    def fan_urls(self,response):

        fan_urls_list = response.xpath('//div[@class="ui divided items"]//div[@class="item"]')
        for fan in fan_urls_list:
            # 粉丝的URL
            fan_url = fan.xpath('div[@class="content"]//a/@href').extract()[0]
            # 继续追踪粉丝(粉丝本身也是一个独立的博主)的粉丝数和关注数.
            yield scrapy.Request(fan_url, callback=self.fans_list)


        # 粉丝列表的下一页的标志是否存在
        next_page_flag_exist = response.xpath('//div[@class="ui pagination menu"]//a[last()]/text()')
        if next_page_flag_exist :
            if response.xpath('//div[@class="ui pagination menu"]//a[last()]/@href'):
                next_page_url = response.request.url.split('followers')[0]+'followers'+ response.xpath('//div[@class="ui pagination menu"]//a[last()]/@href').extract()[0]
                # print("====粉丝列表下一页的url为:",next_page_url)
                yield scrapy.Request(next_page_url,callback=self.fan_urls)
            else:
                # print("====={0}=====已经到本博客的最后一页,跳过==============".format(response.request.url))
                pass
        else:
            # print("============下一页不存在,跳过==============")
            pass

    def bloger_follow_list(self,response):
        # 博主关注者数量
        blog_follower_number = response.xpath('//div[@class="ui three tiny statistics user-statistics"]//a[3]//div[@class="value"]/text()').extract()[0].replace('\n','').replace('\r','').replace(' ','')

        if  blog_follower_number != '0' :
            # 打印一下博主关注者数量,然后判断一下
            follow_list = response.xpath('//div[@class="followers-wrap"]//div[3]//div[@class="ui divided items"]')

            for follower in follow_list:
                #该博主的关注者的url
                follow_url = follower.xpath('div[@class="item friend-item"]//div[@class="content"]//a/@href').extract()[0]
                # 将该博主的关注者的url抛入管道.

                yield scrapy.Request(follow_url,callback=self.fans_list)

            # 关注列表的下一页的标志是否存在
            next_page_flag_exist = response.xpath('//div[@class="ui pagination menu"]//a[last()]/text()')
            if next_page_flag_exist:
                if response.xpath('//div[@class="ui pagination menu"]//a[last()]/@href'):
                    next_page_url = response.request.url.split('following')[0] + 'following' + \
                                    response.xpath('//div[@class="ui pagination menu"]//a[last()]/@href').extract()[0]
                    # print("下一页的url为:", next_page_url)
                    yield scrapy.Request(next_page_url, callback=self.bloger_follow_list)
                else:
                    # print("====={0}  <---已经到本博客的最后一页,跳过==============".format(response.request.url))
                    pass
            else:
                # print("============下一页不存在,跳过==============")
                pass
        else:
            print("============该博主的关注者数量为0,跳过==============")


    def fan_index_next_page(self,response):
        blog_article_list = response.xpath('//div[@id="mainScreen"]//div[@class="ui container"]//div//div[@class="item blog-item"]')
        if blog_article_list:
            # print("========该博主存在文章列表=====")
            item = MasterredistestItem()
            item['url'] = response.request.url
            yield item

            current_page_number = response.request.url.split('p=')[1]
            next_page_url = response.request.url.split('p=')[0] +'p='+str(int(current_page_number)+1)
            yield scrapy.Request(next_page_url,callback=self.fan_index_next_page)

        else:
            # print("=====该博主本页无文章列表====")
            pass







