# -*- coding: utf-8 -*-
import scrapy

from MasterRedisTest.items import MasterredistestItem


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    # allowed_domains = ['https://www.cnblogs.com/']
    start_urls = ['https://www.cnblogs.com']

    def parse(self, response):
        items = MasterredistestItem()
        items['url'] = response.request.url
        yield items         # 将博客园首页的url抛入管道.

        nav_title_list = response.xpath('//div[@id="cate_title_block"]//ul[@id="cate_item"]//li//a/text()').extract()
        nav_url_list = response.xpath('//div[@id="cate_title_block"]//ul[@id="cate_item"]//li//a/@href').extract()
        nav_url_list = [response.url.rstrip('/') + x for x in nav_url_list]
        del nav_title_list[-1]
        del nav_url_list[-1]
        for item in nav_url_list:
            its = MasterredistestItem()
            its['url'] = item
            print("首次的url：",item)
            yield its

        recommend_blog_url = 'https://www.cnblogs.com/aggsite/UserStats'
        yield scrapy.Request(recommend_blog_url,callback=self.recommend_blog_list)

    def recommend_blog_list(self,response):
        recommend_blog = response.xpath('//div[@class="w_l"]//div//ul//li')
        for it in recommend_blog:

            url = "https:" +it.xpath('a/@href').extract()[0]
            if url == 'https://www.cnblogs.com/AllBloggers.aspx': # 此为博客列表(积分排名前3000名的博客列表),单独提取
                yield scrapy.Request(url,callback=self.AllBloggers)
            else:
                item = MasterredistestItem()
                item['url'] = url
                yield item

    def AllBloggers(self,response):
        url_list = response.xpath('/html/body/table[2]//tbody//tr//td//a[1]/@href').extract()
        # print("================博客列表(积分排名前3000名的博客列表)============")
        for url in url_list:
            item = MasterredistestItem()
            item['url'] = url
            yield item