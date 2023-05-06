from django.urls import path
from . import views, api

from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('cron/', views.cron, name='cron'),
    path('play_action/', views.play_action, name='play_action'),
    path('messages/', views.messages, name='messages'),
    path('ranking/', views.ranking, name='ranking'),

    # API ENDPOINTS
    path('api/get_ranking', api.getRanking, name="getRanking"),
]