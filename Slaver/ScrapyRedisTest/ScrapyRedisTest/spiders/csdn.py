import hashlib
import json
import time

import scrapy

from ScrapyRedisTest.items import ScrapyredistestItem, ScrapyredistestItems

from scrapy_redis.spiders import RedisSpider



class csdnSpider(RedisSpider):

    name = 'csdn'
    redis_key = 'csdn:start_urls'


    def parse(self, response):
        """
        分布式爬虫:Slaver端爬虫
        :param response:
        :return:
        """
        if 'api' in response.request.url and 'category' in response.request.url :
            # 如果此url 中包含字符串 'api' 和 'category',说明返回的值是json数据.回调函数为json
            yield scrapy.Request(response.request.url,callback=self.json_data_parse)
        else:
            yield scrapy.Request(response.request.url,callback=self.article_list_data_parse)

    def json_data_parse(self,response):
        """
        返回值为json数据,调用该回调函数.
        :param response:
        :return:
        """
        # 拿到json数据
        number_count = 0
        datas = json.loads(response.text)["articles"]
        for data in datas:
            # 将我们需要的数据都解析出来 并交给CsdnhomepagePipeline管道处理
            item = ScrapyredistestItems()
            item["article_type"] = data['category']
            item["nick_name"] = data['nickname']
            item["article_title"] = data['title']
            item["article_link"] = data['url']
            item["article_desc"] = data['desc']
            item["comments"] = data['comments']  # 评论
            item["digg"] = data['digg']  # 点赞
            item["user_name"] = data['user_name']  # 用户id
            item["views"] = data['views']  # 用户views
            item["source"] = "CSDN"
            item["article_img"] = "无"
            item["user_url"] = data['user_url']   # 用户博客主页的url
            item["user_img"] = data['avatarurl']  # 用户头像的图片url
            number_count +=1
            yield item

            user_url =  data['user_url']
            meta_json = {'user_url': item["user_url"], 'user_img': item["user_img"],
                         'user_name':item["user_name"],'nick_name':item["nick_name"]}
            print(meta_json)
            yield scrapy.Request(user_url,meta=meta_json,callback=self.article_list_data_parse)


    def article_list_data_parse(self,response):
        list_number_count = 0
        print(">" * 20 + "User详情页爬取." + "<" * 20)
        article_type = "博客"

        article_img = '无'  # 因 "csdn" 的文章列表中不存在文章插图，故暂时显示：无
        article_list = response.xpath('//div[@class="article-list"]//div[@class="article-item-box csdn-tracking-statistics"]')
        for article_item in article_list:
            list_number_count += 1
            it = ScrapyredistestItems()
            nick_name = ''.join(response.xpath('//a[@id="uid"]/span/text()').extract()).replace('\n', '').replace(' ','')
            user_name = ''.join(response.xpath('//a[@id="uid"]//span/@username').extract()).replace('\n', '').replace(' ','')
            it['article_title'] =''.join(article_item.xpath('h4/a/text()').extract()).replace('\n','').replace(' ','')
            it['article_desc'] =''.join(article_item.xpath('p/a/text()').extract()).replace('\n','').replace(' ','')
            it['article_link']= ''.join(article_item.xpath('h4/a/@href').extract())
            it['views'] =''.join( article_item.xpath('div/p[3]/span/span/text()').extract())
            it['comments'] =''.join( article_item.xpath('div/p[5]/span/span/text()').extract())
            it['digg'] = '--'
            it['source'] = "CSDN"
            it['article_type'] = article_type
            it['nick_name'] = nick_name
            it['user_name'] = user_name
            it['user_url'] = response.xpath("//div[@id='mainBox']/aside[@class='blog_container_aside']/div[@id='asideProfile']/div[@class='profile-intro d-flex']/div[@class='user-info d-flex flex-column profile-intro-name-box']/div[1]/a[@id='uid']/@href").extract()
            it['user_img'] = response.xpath("//div[@id='mainBox']/aside[@class='blog_container_aside']/div[@id='asideProfile']/div[@class='profile-intro d-flex']/div[@class='avatar-box d-flex justify-content-center flex-column']/a/img[@class='avatar_pic']/@src").extract()
            it['article_img'] = article_img
            print("==========nick_name:",nick_name)
            print("==========user_name:",user_name)
            print("==========user_url:",it["user_url"])
            print("==========user_img:",it["user_img"])

            # print(it)
            yield  it

        # 下一页
        print("===================下一页==========================")
        pageBox = response.xpath('//div[@id="pageBox"]')

        if pageBox and 'article/list' not in response.request.url:
            listTotal_String = response.body.decode('utf-8').split('listTotal')[1].split('pageQueryStr')[0].replace(
                '=', '').replace(';', '').replace(' ', '').replace('var', '')
            listTotal = int(listTotal_String) // 40 + 1
            print(listTotal, '*********************************************8')
            for i in range(2, listTotal + 1):
                print("==============页数存在==============")
                url = response.request.url.split('article')[0] + '/article/list/' + str(i)
                print("此时的url为：", url)

                yield scrapy.Request(url, callback=self.article_list_data_parse)
        else:
            print("==========此博客只有一页.已经爬取结束,跳过.====================")

        print("===================结束==========================")



