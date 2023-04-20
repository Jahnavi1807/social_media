from django.urls import path
from App_Posts import views
from App_Posts.views import search_news
app_name = "App_Posts"

urlpatterns = [
  
   path("",views.home , name='home'),
   path("liked/<pk>/",views.liked , name='liked'),
   path("unliked/<pk>/",views.unliked , name='unliked'),
   path('news/', search_news, name='search_news'),

]
