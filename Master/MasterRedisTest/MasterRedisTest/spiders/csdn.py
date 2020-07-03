# -*- coding: utf-8 -*-
import json
import random
import time

import scrapy

from MasterRedisTest.function import category_url_list
from MasterRedisTest.items import MasterredistestItem


class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    # allowed_domains = ['www.csdn.net/']
    start_urls = ['http://www.csdn.net/']

    def parse(self, response):
        """
        获取CSDN的nav分类:home,wetchers,career,python,java,web,arch,db,5g,game,mobile,ops,sec,engineering,iot,fund,avi,other
        以当前时间戳拼凑url,循环100次.
        :param response:
        :return:
        """
        nav_url_list = response.xpath('//div[@class="clearfix"]//div[@class="nav_com"]//ul//li//a/@href').extract()
        http_url_list, nav_letter = category_url_list(nav_url_list)
        for item in nav_letter:
            for i in range(0, 101):
                time.sleep(1)
                it = MasterredistestItem()
                # 拿到当前时间戳 拼接成url
                url_time = int(time.time() * 1000000)
                url = "https://www.csdn.net/api/articles?type=more&category={0}&shown_offset=".format(item) + str(
                    url_time)
                it['url'] = url
                yield it
                yield scrapy.Request(url, callback=self.detail_parse)


            # url 类型type为new 的字符串拼接，并循环100次.
            for j in range(0,101):
                its = MasterredistestItem()
                url_time = int(time.time() * 1000000)
                type_new_url = 'https://www.csdn.net/api/articles?type=new&category={0}&shown_offset='.format(item)+ str(url_time)
                its['url'] = type_new_url
                yield its
                yield scrapy.Request(type_new_url, callback=self.detail_parse)



        # 随机获取 6页 博客专家列表页数据,回调函数为weekList,
        # 两步：一:获取博客专家的个人博客列表页url;二:获取此博客专家的粉丝的个人博客列表页url
        for k in range(1,6):
            k = random.randint(0,7)
            week_url = 'https://blog.csdn.net/api/WritingRank/weekList?page='+str(k)
            yield scrapy.Request(week_url,callback=self.weekList)




    def detail_parse(self,response):
        # 拿到json数据
        datas = json.loads(response.text)["articles"]
        for data in datas:
            item = MasterredistestItem()
            # 将我们需要的数据都解析出来 并交给CsdnhomepagePipeline管道处理
            item["url"] = data['user_url']
            yield item

            # 通过blog 个人博客列表页的url ,找出其粉丝的个人博客列表页
            me_url = data['user_url'].replace('blog', 'me')
            fans_url = me_url.split('me.csdn.net')[0] + 'me.csdn.net' + '/fans' + me_url.split('me.csdn.net')[1]
            yield scrapy.Request(fans_url, callback=self.fans_parse)


    def fans_parse(self,response):
        fans_count = response.xpath('//div[@class="sub_button"]/a[1]/span[1]/text()').extract()[0]
        if fans_count!= '0':
            fans_lsit = response.xpath('//div[@class="chanel_det_list clearfix"]//ul/li[@class="item clearfix"]/a[1]/@href').extract()
            for fan_url in fans_lsit:
                fan_item = MasterredistestItem()
                fan_item["url"] = fan_url.replace('me','blog')
                yield fan_item


    def weekList(self,response):
        print("===============解析博客专家的url列表================")
        code = json.loads(response.text)["code"]
        if int(code) == 200:
            datas = json.loads(response.text)["data"]["list"]
            for data in datas:
                username = data["username"]
                week_url = 'https://blog.csdn.net/' + username
                # print("===============博客专家的url列表================", week_url)
                yield week_url   # 抛出 博客专家的url.

                # 通过blog 个人博客列表页的url ,找出其粉丝的个人博客列表页
                me_url = week_url.replace('blog', 'me')
                fans_url = me_url.split('me.csdn.net')[0] + 'me.csdn.net' + '/fans' + me_url.split('me.csdn.net')[1]
                # print("==================week_fans_url:", fans_url)

                yield scrapy.Request(fans_url, callback=self.fans_parse)


