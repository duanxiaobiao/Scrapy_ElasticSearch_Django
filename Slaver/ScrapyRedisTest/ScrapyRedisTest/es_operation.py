
# -*- coding:utf-8 -*-

from elasticsearch_dsl import DocType,Completion,Text,Keyword,Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
# 新建连接
from ScrapyRedisTest.settings import ELASTICSEARCH_INDEX, ELASTICSEARCH_TYPE

connections.create_connection(hosts="localhost")
# 设置搜索建议字段
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word",filter=["lowercase"])

class ArticleType(DocType):
    ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])
    suggest = Completion(analyzer=ik_analyzer)  # 自动补全
    article_type = Keyword()                     # 文章类型
    nick_name = Keyword()                        # 昵称
    article_title = Text(analyzer="ik_max_word")                    # 文章标题
    article_link = Keyword()                     # 文章链接
    article_desc = Text(analyzer="ik_max_word")  # 文章描述
    comments = Keyword()                         # 文章评论
    digg = Keyword()                             # 文章点赞数
    user_name = Keyword()                        # user用户名
    views = Keyword()                            # 观看数
    source = Keyword()                           # 来源
    article_img = Keyword()                      # 文章中的图片
    user_url = Keyword()                         # 用户博客主页的URL
    user_img = Keyword()                         # 用户头像的url

    class Meta:
        # 数据库名称和表名称
        index = ELASTICSEARCH_INDEX
        doc_type = ELASTICSEARCH_TYPE

if __name__ == '__main__':
    try:
        ArticleType.init()
        print("ElasticSearch 索引创建成功")
    except Exception as e:
        print("ElasticSearch索引创建失败")
        print(e)

