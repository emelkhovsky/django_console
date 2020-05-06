from . import views
from django.urls import path
from django.conf.urls import url

app_name = 'riddles'

urlpatterns = [
    path('', views.main, name = 'main'),
    path('reg/', views.reg, name = 'reg'),
    path('login/', views.login, name = 'login'),
    path('progress/', views.progress, name = 'progress'),
    path('lesson1/', views.lesson1, name='lesson1'),
    path('lesson2/', views.lesson2, name='lesson2'),
    path('lesson3/', views.lesson3, name='lesson3'),
    path('lesson4/', views.lesson4, name='lesson4'),
    path('lesson5/', views.lesson5, name='lesson5'),
    path('lesson6/', views.lesson6, name='lesson6'),
    url('create_post/', views.create_post, name='create_post'),

]