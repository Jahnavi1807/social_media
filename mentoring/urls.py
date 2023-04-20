
from django.urls import path
from mentoring import views

app_name = 'mentoring'

urlpatterns = [
    path('', views.index, name='index'),
    path('mentorship_list/', views.mentorship_list, name='mentorship_list'),
    path('request/', views.mentorship_request, name='request'),
    path('requests/', views.mentorship_requests, name='requests'),
    path('<int:pk>/accept/', views.mentorship_request_acceptance, name='accept_request'),
]
