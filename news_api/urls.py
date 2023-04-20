from django.urls import path
from news_api import views

urlpatterns = [
    path('', views.news, name='news'),
]