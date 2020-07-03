import datetime
import json
import random
import xml

import jieba
from django.forms import model_to_dict
from django.http import HttpResponse
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from elasticsearch_dsl.connections import Connections
from pip._vendor import requests

from DjangoSearch.settings import ELASTICSEARCH_INDEX
from search import pagination, models
from search.functions import XMLHandler, random_search_key, random_recommend, jieba_participle, search_body, spiderview
from search.models import ArticleType, User

connection = Connections()
client = connection.create_connection(hosts=['127.0.0.1'], timeout=20)


class RandomRecommendView(View):

    def get(self,request):
        """
        :param request: 随机推荐函数.
        :return:随机推荐的10条数据
        """
        uid = request.GET.get("uid","null")

        try:
            if uid != "null":
                print("此时用户状态是：[已登录]")
                # 如果用户状态为登录状态：
                # 此时推荐功能为：使用该用户的历史搜索记录通过结巴分词,分析出词频较高的关键字
                search_key_list = models.User_Search_Key.objects.filter(uid = int(uid))
                if len(search_key_list) != 0:
                    keys_list =','.join([ item.search_key for item in search_key_list])
                    wcls = jieba_participle(keys_list)
                    key_word = wcls[0][0]
                    response = client.search(index=ELASTICSEARCH_INDEX,body=random_search_key(key_word))
                else:
                    print("此时数据库中搜索字段为空!随机返回10条数据")
                    response = client.search(index=ELASTICSEARCH_INDEX, body=random_recommend())
            else:
                print("此时用户状态是：[未登录]")
                # 用户未登录情况下使用随机返回10条数据.
                response = client.search(index=ELASTICSEARCH_INDEX,body=random_recommend())

            info_list = []
            info_list.append(response)
            return HttpResponse(json.dumps({"status": 200, "response": info_list}, ensure_ascii=False))

        except Exception as e:
            print("[异常]",e)
            return HttpResponse(json.dumps({"status": -1, "response": "查询异常,请检查相关原因"}, ensure_ascii=False))


    def post(self,request):
        return HttpResponse(json.dumps({"status": -1, "response": request.method +' invaild.'}, ensure_ascii=False))




class SearchView(View):
    """
    搜索视图
    """
    def get(self,request):
        start_time = datetime.datetime.now()
        keyword = request.GET.get("keyword")
        cur_page = request.GET.get("cur_page",1)
        UID = request.GET.get("uid","null")
        print("UID：",UID)
        if UID != "null" :
            print("此时用户状态为:[已登录] -->用户登录的情况下，收集用户的搜索关键词,存储数据库进行分析.")
            search_key_list = models.User_Search_Key.objects.all()
            if len(search_key_list) != 0:
                last_search_key = models.User_Search_Key.objects.last().search_key
                if last_search_key !=keyword:
                    models.User_Search_Key.objects.create(uid_id=int(UID), search_key=keyword)
                    print("搜索关键词存储成功!")
        else:
            print("此时用户状态为:[未登录]")
        try:
            response = client.search(index=ELASTICSEARCH_INDEX,body=search_body(keyword,cur_page))
            info_list = []
            info_list.append(response)
            page_dict = {}
            page_obj = pagination.Pagination(cur_page, response.get("hits").get("total"), 10)
            page_dict['cur_page'] = cur_page
            page_dict['page_start'] = page_obj.page_start
            page_dict['page_end'] = page_obj.page_end
            page_dict['last_page'] = page_obj.total_page_num
            page_dict['data_count'] = response.get("hits").get("total")
            end_time = datetime.datetime.now()
            time_consume = (end_time - start_time).microseconds/1000
            page_dict['time_consume'] = time_consume
            info_list.append(page_dict)
            return HttpResponse(json.dumps({"status":200,"response":info_list},ensure_ascii=False))
        except Exception as e:
            print("[异常]:",e)
            return HttpResponse(json.dumps({"status":-1,"response":"查询异常,请检查相关原因"},ensure_ascii=False))

    def post(self,request):
        return HttpResponse(json.dumps({"status": -1, "response": request.method + ' invaild.'}, ensure_ascii=False))




class SuggestView(View):
    """
    搜索建议视图
    """
    def get(self,request):
        suggest_keyword = request.GET.get("keyword")
        print("=================================")
        print("搜索关键词:",suggest_keyword)
        print("=================================")
        response_data = []
        if suggest_keyword:
            s = ArticleType.search()
            s= s.suggest("my_suggest",suggest_keyword,completion={"field":"suggest","fuzzy":{"fuzziness":2},"size": 10})
            suggestions = s.execute_suggest()
            for match in getattr(suggestions,"my_suggest")[0].options:
                source = match._source
                response_data.append(source["article_title"])
            if len(response_data)> 10:
                response_data = response_data[:10]
        return HttpResponse(json.dumps({"status":200,"response":response_data},ensure_ascii=False))

    def post(self,request):
        return HttpResponse(json.dumps({"status": -1, "response": request.method + ' invaild.'}, ensure_ascii=False))




class SpiderView(View):

    def get(self,request):
        """
        :param request:
        :return: 返回爬虫的种类和爬取的数量.
        """
        response = client.search(index=ELASTICSEARCH_INDEX,body=spiderview())
        data = response.get("aggregations").get("user_type").get("buckets")
        return HttpResponse(json.dumps({'status':200,'response':data}, ensure_ascii=False))

    def post(self,request):
        return HttpResponse(json.dumps({"status": -1, "response": request.method + ' invaild.'}, ensure_ascii=False))





class LoginView(View):

    def get(self,request):
        return HttpResponse(json.dumps({"status": -1, "response": request.method + ' invaild.'}, ensure_ascii=False))

    def post(self,request):

        loginName = request.POST.get("loginName").replace(' ','')
        password  = request.POST.get("password").replace(' ','')
        if loginName == "" or  password == "" :
            return HttpResponse(json.dumps({"status":-1,"response":"账户名或密码不能为空."},ensure_ascii=False))

        userObject = models.User.objects.filter(user_name= loginName,user_pwd=password)
        if userObject.count() == 0:
            return HttpResponse(json.dumps({"status":-1,"response":"账户名或密码不正确"},ensure_ascii=False))
        else:
            # models.User.objects.create(user_name= loginName,user_pwd=password)
            data = {"uid":models.User.objects.filter(user_name= loginName,user_pwd=password).first().id,'user':loginName,'img':models.User.objects.filter(user_name= loginName,user_pwd=password).first().reserve1}
            return HttpResponse(json.dumps({"status": 200, "response": data}, ensure_ascii=False))







class RegisterView(View):

    def get(self,request):
        return HttpResponse(json.dumps({"status": -1, "response": request.method + ' invaild.'}, ensure_ascii=False))

    @csrf_exempt
    def post(self,request):
        loginName = request.POST.get("loginName").replace(' ','')
        password = request.POST.get("password").replace(' ','')
        telphone = request.POST.get("telphone").replace(' ','')
        message_code = request.POST.get("message_code").replace(' ','')
        nameObject = models.User.objects.filter(user_name = loginName).count()
        userObject = models.User.objects.filter(user_telphone=telphone).count()
        if nameObject != 0 :
            return HttpResponse(json.dumps({'status':-1,'response':"账户名称重复,请重新输入"}, ensure_ascii=False))
        if userObject != 0 :
            return HttpResponse(json.dumps({'status': -1, 'response': "手机号已经被注册,请重新输入"}, ensure_ascii=False))

        session_message_code = request.session.get("message_code")
        if  str(message_code) == str(session_message_code):
            models.User.objects.create(user_name= loginName,user_pwd = password,user_telphone = telphone,reserve1="/static/images/ddy.jpg")
            return HttpResponse(json.dumps({'status': 200, 'response': "注册成功!"}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'status': -1, 'response': "注册失败!请重新注册!"}, ensure_ascii=False))





class Send_MessageView(View):

    def get(self,request):
        # 获取ajax的get方法发送过来的手机号码
        mobile = request.GET.get('mobile')
        # 通过手机去查找用户是否已经注册
        user = User.objects.filter(user_telphone=mobile)
        if len(user) == 1:
            return HttpResponse(json.dumps({"status": -1, "response": "该手机已经被注册"}, ensure_ascii=False))
        # 定义一个字符串,存储生成的6位数验证码
        message_code = ''
        for i in range(6):
            i = random.randint(0, 9)
            message_code += str(i)
        # 拼接成发出的短信
        text = "您的验证码是：" + message_code + "。请不要把验证码泄露给其他人。"
        # return HttpResponse(json.dumps({"status":200,"response":"ok"},ensure_ascii=False))
        ## 请求地址
        url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"

        # APIID
        account = "C14788130"
        # APIkey
        password = "8f4b16c05f68f4007beace74bacc45f0"

        ## 收件人手机号
        mobile = mobile
        ## 短信内容
        content = text
        ## 请求头
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }
        ## 构建发送参数
        data = {
            "account": account,
            "password": password,
            "mobile": mobile,
            "content": content,
        }
        ## 发送
        response = requests.post(url, headers=headers, data=data)
        # url    请求地址
        # headers  请求头
        # data 请求数据  内容
        print(response.content.decode('utf-8'))
        xh = XMLHandler()
        xml.sax.parseString(response.content.decode('utf-8'), xh)
        ret = xh.getDict()
        msg= ret.get("msg")
        if msg == '提交成功':
            request.session['message_code'] = message_code
            # request.session.set_expiry(61)
            return HttpResponse(json.dumps({'status':200,'response':"验证码发送成功!"},ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({'status': -1, 'response': "验证码发送失败,请重新尝试发送"}, ensure_ascii=False))

    def post(self,request):
        return HttpResponse(json.dumps({"status": -1, "response": request.method + ' invaild.'}, ensure_ascii=False))







class BlogerRecommendView(View):

    def get(self,request):
        try:
            info = []
            response = client.search(index=ELASTICSEARCH_INDEX, body={
                "size": 0,
                "aggs": {
                    "nick_name": {
                        "terms": {
                            "field": "nick_name"
                        }
                    }
                }
            })
            datas = response.get("aggregations").get("nick_name").get("buckets")
            for data in datas:
                res = client.search(index=ELASTICSEARCH_INDEX, body={
                    "from": 0,
                    "size": 1,
                    "query": {
                        "match": {
                            "nick_name": data.get('key')
                        }
                    }
                })
                UID = res.get("hits").get("hits")[0].get("_source").get("article_link").replace('//','*').split('/')[1]
                domain = res.get("hits").get("hits")[0].get("_source").get("article_link").replace('//','*').split('/')[0].replace('*','//')
                url = domain+'/'+UID
                data["url"] = url
                info.append(data)

            return HttpResponse(json.dumps({'status': 200, 'response': info}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({'status': -1, 'response': "查询异常"}, ensure_ascii=False))

    def post(self,request):
        return HttpResponse(json.dumps({"status": -1, "response": request.method + ' invaild.'}, ensure_ascii=False))