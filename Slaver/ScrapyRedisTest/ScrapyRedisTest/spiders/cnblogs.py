

import json
import time

import scrapy

from ScrapyRedisTest.function import category_url_list, String_Cleaning
from ScrapyRedisTest.items import ScrapyredistestItem, ScrapyredistestItems
from scrapy_redis.spiders import RedisSpider


class cnblogSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'cnblogs'
    redis_key = 'cnblogs:start_urls'


    def parse(self, response):
        if 'signin' in response.request.url and 'ReturnUrl' in response.request.url:
            print("此url类似:=={}==,不满足爬取条件,跳过.".format(response.request.url))
            pass
        else:
            url_item_list =[ i for i in response.request.url.replace('https://','').split('/') if i!='']
            if len(url_item_list) == 2:
                yield scrapy.Request(response.request.url,callback=self.Person_blog_List)
            else:
                yield scrapy.Request(response.request.url, callback=self.Category_blog_List)


    def Person_blog_List(self,response):
        """
        :param response: 个人博客列表回调函数.
        :return:
        """
        print("=============分类博客列表URL：=======", response.request.url)
        article_list = response.xpath('//div[@class="day"]')
        for article in article_list:
            item = ScrapyredistestItems()
            item['article_title'] = article.xpath('div[@class="postTitle"]//a/text()').extract()[0]
            item['article_link'] = article.xpath('div[@class="postTitle"]//a/@href').extract()[0]
            item['article_type'] = '博客'
            item['nick_name'] = article.xpath("div[@class='postDesc']/text()").extract()[0].split('阅读')[0].split('posted')[1].split(' ')[-2]
            item['article_desc'] = String_Cleaning(''.join(article.xpath('div[@class="postCon"]//div[@class="c_b_p_desc"]/text()').extract()))
            comments = article.xpath("div[@class='postDesc']/text()").extract()[0]
            item["comments"] = String_Cleaning(comments.split('评论')[1]).replace('(', '').replace(')', '')

            item["article_img"] = "无"  # 文章中的图片    11
            item["user_img"] = "列表页，暂无url提取"  # 用户头像的url
            item["user_url"] = response.request.url  # 用户博客主页的URL
            item['digg'] = '--'
            item['user_name'] = response.request.url.rstrip('/').split('/')[-1]

            item['views'] = article.xpath("div[@class='postDesc']/text()").extract()[0].split('阅读')[1].split('评论')[
                0].replace('(', '').replace(')', '')
            item['source'] = "博客园"
            yield  item

        next_page = String_Cleaning(''.join(response.xpath('//div[@id="nav_next_page"]//a/text()').extract()))
        second_page = response.xpath(
            '//div[@id="homepage_bottom_pager"]//div[@class="pager"]//a[last()]/text()').extract()

        if "下一页" in next_page or "下一页" in second_page:  #
            print("============下一页存在!!=====================")
            if "下一页" in next_page:
                next_url = response.xpath('//div[@id="nav_next_page"]//a/@href').extract()[0]
                print("============下一页的url:=========", next_url)
                yield scrapy.Request(next_url, callback=self.Person_blog_List)
            if "下一页" in second_page:
                next_url = response.xpath('//div[@id="homepage_bottom_pager"]//div[@class="pager"]//a[last()]/@href').extract()[0]
                print("============下一页的url:=========", next_url)
                yield scrapy.Request(next_url, callback=self.Person_blog_List)
        else:
            pass

    def Category_blog_List(self,response):
        print("=============分类博客列表URL：=======", response.request.url)

        article_list = response.xpath('//div[@id="post_list"]//div[@class="post_item"]')
        for it in article_list:
            item = ScrapyredistestItems()
            item['article_type'] = "博客"
            item['nick_name'] = it.xpath('div[@class="post_item_body"]//div[@class="post_item_foot"]/a/text()').extract()[0]

            item["article_img"] = "无"  # 文章中的图片    11
            item["user_img"] = it.xpath('div[@class="post_item_body"]//p//a/img/@src').extract()    # 用户头像的url
            item["user_url"] = it.xpath('div[@class="post_item_body"]//p//a/@href').extract()  # 用户博客主页的URL
            print("============user_img:",item["user_img"])
            print("============user_url:",item["user_url"])
            item['article_title'] = it.xpath('div[@class="post_item_body"]/h3/a/text()').extract()[0]
            item['article_link'] = it.xpath('div[@class="post_item_body"]/h3/a/@href').extract()[0]
            item['article_desc'] = it.xpath('div[@class="post_item_body"]/p[[@class="post_item_summary"]/text()').extract()[0]
            item['comments'] = it.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/span[1]/a/text()').extract()[0].replace(
                '评论', '').replace('(', '').replace(')', '').replace(' ', '').replace('\r\n', '')  # 评论
            item['digg'] = it.xpath('div[@class="digg"]/div[@class="diggit"]/span/text()').extract()[0]
            item['user_name'] = item['nick_name']
            item['views'] = it.xpath('div[@class="post_item_body"]/div[@class="post_item_foot"]/span[2]/a/text()').extract()[0].replace(
                    '阅读', '').replace('(', '').replace(')', '').replace(' ', '').replace('\r\n', '')
            item['source'] = "博客园"
            yield item
            user_url = it.xpath('div[@class="post_item_body"]//div[@class="post_item_foot"]/a/@href').extract()[0]
            yield scrapy.Request(user_url,callback=self.Person_blog_List)


        # 下一页：
        next_page_flag = response.xpath(
            '//div[@id="pager_bottom"]//div[@id="paging_block"]//div[@class="pager"]//a[last()]/text()').extract()[0]
        next_page_url = response.xpath(
            '//div[@id="pager_bottom"]//div[@id="paging_block"]//div[@class="pager"]//a[last()]/@href').extract()[0]

        next_url = 'https://www.cnblogs.com' + next_page_url

        print("爬取的url为：", response.request.url, '   ', "下一页的url为：", next_url)
        if 'Next' in next_page_flag:
            # 存在下一页,继续循环
            yield scrapy.Request(next_url, callback=self.Category_blog_List)
        else:
            print("=======不存在下一页,跳过==========")
