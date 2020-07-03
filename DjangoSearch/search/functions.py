import xml.sax
import xml.sax.handler

import jieba


class XMLHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.mapping = {}

    def startElement(self, name, attributes):
        self.buffer = ""

    def characters(self, data):
        self.buffer += data

    def endElement(self, name):
        self.mapping[name] = self.buffer

    def getDict(self):
        return self.mapping


# data = '<?xml version="1.0" encoding="utf-8"?><SubmitResult xmlns="http://106.ihuyi.com/"><code>2</code><msg>提交成功</msg><smsid>15870246956696820530</smsid></SubmitResult>'
#
# xh = XMLHandler()
# xml.sax.parseString(data.encode(), xh)
# ret = xh.getDict()

def random_search_key(key_word):
    """
    :param key_word:用户登录状态：[已登录] --> 推荐功能使用的body字典
    :return:
    """
    body = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"article_title": key_word}},
                        {"match": {"article_desc": key_word}}
                    ]
                }
            },
            "size": 10,
            "sort": {
                "_script": {
                    "script": "Math.random()",
                    "type": "number",
                    "order": "asc"
                }
            }
            # ,"_source": {
            #   "includes": [
            #     "article_title",
            #     "article_link",
            #     "article_desc",
            #     "nick_name",
            #     "comments",
            #     "digg",
            #     "user_name",
            #     "views",
            #     "source",
            #   ],
            #   "excludes": []
            # }
        }
    return body



def random_recommend():
    """
    用户登录状态：[未登录] --> 推荐功能使用的body字典
    :return:
    """
    body = {
        "size": 10,
        "sort": {
            "_script": {
                "script": "Math.random()",
                "type": "number",
                "order": "asc"
            }
        }
        # ,"_source": {
        #   "includes": [
        #     "article_title",
        #     "article_link",
        #     "article_desc",
        #     "nick_name",
        #     "comments",
        #     "digg",
        #     "user_name",
        #     "views",
        #     "source",
        #   ],
        #   "excludes": []
        # }
    }
    return body


def search_body(keyword,cur_page):
    body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"article_title": keyword}},
                    {"match": {"article_desc": keyword}}
                ]
            }
        },
        "from": (int(cur_page) - 1) * 10,
        "size": 10,
        "highlight": {
            "pre_tags": '<span class="keyWord">',
            "post_tags": '</span>',
            "fields": {
                "article_title": {},
                "article_desc": {}
            }
        }
    }

    return body

def spiderview():
    body = {
                "size": 0,
                "aggs": {
                    "user_type": {
                        "terms": {
                            "field": "source"
                        }
                    }
                }
            }
    return body



def jieba_participle(text):
    """
    :param text: 结巴分词(participle) : 通过对字符串进行结巴分词,提取出现较高的词频.
    :return:
    """
    wordsls = jieba.lcut(text)
    wcdict = {}
    for word in wordsls:
        if len(word) == 1:
            continue
        else:
            wcdict[word] = wcdict.get(word, 0) + 1
    wcls = list(wcdict.items())
    wcls.sort(key=lambda x: x[1], reverse=True)
    return  wcls




