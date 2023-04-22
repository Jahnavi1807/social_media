from django.urls import path
from news_api import views

app_name='news_api'

urlpatterns = [
    path('', views.news, name='news'),

]