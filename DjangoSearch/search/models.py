from django.db import models

# Create your models here.

# -*- coding:utf-8 -*-
from django.utils import timezone

from elasticsearch_dsl import DocType,Nested,Date,Boolean,analyzer,Completion,Text,Keyword,Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
# 新建连接
from DjangoSearch.settings import ELASTICSEARCH_INDEX, ELASTICSEARCH_TYPE

connections.create_connection(hosts="127.0.0.1")
# 设置搜索建议字段
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word",filter=["lowercase"])

class ArticleType(DocType):
    suggest = Completion(analyzer=ik_analyzer)  # 自动补全
    article_type = Keyword()                     # 文章类型
    nick_name = Keyword()                        # 昵称
    article_title = Keyword()                    # 文章标题
    article_link = Keyword()                     # 文章链接
    article_desc = Text(analyzer="ik_max_word")  # 文章描述
    comments = Keyword()                         # 文章评论
    digg = Keyword()                             # 文章点赞数
    user_name = Keyword()                        # user用户名
    views = Keyword()                            # 观看数
    source = Keyword()                           # 来源

    class Meta:
        # 数据库名称和表名称
        index = ELASTICSEARCH_INDEX
        doc_type = ELASTICSEARCH_TYPE


class User(models.Model):
    """
    用户登录注册表
    """
    user_name = models.CharField(max_length=128,verbose_name="用户名")
    user_pwd = models.CharField(max_length=128,verbose_name="用户密码")
    user_telphone  = models.CharField(max_length=128,verbose_name="用户手机号")

    reserve1  = models.CharField(max_length=128,verbose_name="保留字段1")
    reserve2  = models.CharField(max_length=128,verbose_name="保留字段2")
    reserve3  = models.CharField(max_length=128,verbose_name="保留字段3")
    reserve4  = models.CharField(max_length=128,verbose_name="保留字段4")

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = "User"
        verbose_name_plural = '用户表'


class User_Search_Key(models.Model):

    uid = models.ForeignKey('User',on_delete=models.CASCADE)

    search_key = models.CharField(max_length=128,verbose_name="用户搜索关键词")

    search_time = models.DateTimeField('搜索时间', default=timezone.now)

    reserve1 = models.CharField(max_length=128, verbose_name="保留字段1")
    reserve2 = models.CharField(max_length=128, verbose_name="保留字段2")
    reserve3 = models.CharField(max_length=128, verbose_name="保留字段3")
    reserve4 = models.CharField(max_length=128, verbose_name="保留字段4")

    def __str__(self):
        return self.search_key

    class Meta:
        db_table = "User_Search_Key"
        verbose_name_plural = '用户搜索关键词表'




if __name__ == '__main__':
    ArticleType.init()

