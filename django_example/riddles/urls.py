from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'riddles'

urlpatterns = [
    path('', views.main, name = 'main'),
    path('reg/', views.reg, name = 'reg'),
    path('console/', views.console, name = 'console'),
]