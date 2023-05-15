from django.urls import path
from . import views, api

from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('cron/', views.cron, name='cron'),
    path('play_action/', views.play_action, name='play_action'),
    path('messages/', views.messages, name='messages'),
    path('ranking/', views.ranking, name='ranking'),
    path('actions/', views.actions, name='actions'),

    # API ENDPOINTS
    path('api/get_ranking', api.getRanking, name="getRanking"),
    path('api/get_actions', api.getActions, name="getActions"),
    path('api/make_action', api.makeAction, name="makeAction"),
    path('api/get_user', api.getCurrentUser, name="getCurrentUser"),
    path('api/get_gameOptions', api.getGameOptions, name="getGameOptions"),
    path('api/get_events', api.getEvents, name="getEvents"),
    path('api/get_resources', api.getResources, name="getResources"),
    path('api/get_statistics', api.getStatisticsCurrentUser, name="getStatistics"),
]