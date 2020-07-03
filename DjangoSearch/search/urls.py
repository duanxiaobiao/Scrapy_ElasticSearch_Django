from django.urls import path

from search import views
from search.views import *

"""
后端API的路由
"""
urlpatterns = [
    # 搜索接口
    path('random-recommend/',views.RandomRecommendView.as_view()),

    path('bloger-recommend/',views.BlogerRecommendView.as_view()),

    path('search/',views.SearchView.as_view()),
    # 搜索建议接口
    path('suggest/',views.SuggestView.as_view()),
    #
    path('spider-data/',views.SpiderView.as_view()),

    path('login/', LoginView.as_view(), name='login'),

    path('register/', RegisterView.as_view(), name='register'),

    path('send_message/', Send_MessageView.as_view(), name='login'),
]