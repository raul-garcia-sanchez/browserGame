from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cron/', views.cron, name='cron'),
    path('play_action/', views.play_action, name='play_action'),
    path('messages/', views.messages, name='messages'),
    path('ranking/', views.ranking, name='ranking'),
    path('^sign_up/', views.register_user),
    path('^register_success/', views.register_confirm)
]
