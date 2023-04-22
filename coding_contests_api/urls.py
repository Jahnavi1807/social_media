from django.urls import path
from coding_contests_api import views

app_name='coding_contests_api'

urlpatterns = [
    path('', views.contests, name='contests'),

]