from django.urls import path

from front import views

"""前端API的路由
"""
urlpatterns = [
    path('',views.index),
    path('login/',views.login),
    path('register/',views.register),
    path('result/',views.result),




]