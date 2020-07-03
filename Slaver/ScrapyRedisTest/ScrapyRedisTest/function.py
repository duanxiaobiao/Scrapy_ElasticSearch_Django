from elasticsearch_dsl.connections import connections

from ScrapyRedisTest.es_operation import ArticleType

es = connections.create_connection(ArticleType._doc_type.using)

def category_url_list(nav_url_list):
    """
    将CSDN的分类列表的url装进列表
    :param nav_url_list:
    :param response:
    :return:
    """
    http_url_list = []
    nav_letter = []
    for item in nav_url_list:
        if item == '/':
            nav_letter.append('home')
        if 'http' in item:
            http_url_list.append(item)
        if 'nav' in item:
            nav_letter.append(item.split('nav/')[-1])
    return http_url_list,nav_letter

def gen_suggests(index,info_tuple):
    """
    获取字符串生成建议数组
    :param index:
    :param info_tuple:
    :return:
    """
    used_words = set()
    suggests = []
    for text ,weight in info_tuple:
        if text:
            # 调用es 的analyze 接口的
            words = es.indices.analyze(index=index,params={'filter':['lowercase']},body={'text':text,'analyzer':"ik_max_word"})
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = analyzed_words-used_words
        else:
            new_words = set()
        if new_words:
            suggests.append({"input":list(new_words),"weight":weight})

    return suggests


def String_Cleaning(string):
    return string.replace('\r','').replace('\n','').replace(' ','')


