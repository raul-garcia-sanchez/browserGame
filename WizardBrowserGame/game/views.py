from django.shortcuts import render
from .models import *
from django.utils import timezone

# Decorator para refrescar el mana de los usuarios
#( poner: @RefreshResources encima de las vistas en las que se puedan recargar )
from game.decorators import RefreshResources 

# Create your views here.
def index(request, *args, **kwargs):
    context = {}

    return render(request, 'index/index.html', context)

def cron(request):
    context = {}

    return render(request, 'index/cron.html', context)

def play_action(request):
    context = {}

    return render(request, 'index/play_action.html', context)

def messages(request):
    context = {}

    return render(request, 'index/messages.html', context)

def ranking(request):
    context = {}

    return render(request, 'index/ranking.html', context)


# Funcion logs
# Level 1:INFO, 2:SUCCESS , 3:WARNING, 4:ERROR
def InfoLog(user, title, description, route):
    Log.objects.create(
        user=user,
        level=1,
        title=title,
        description=description,
        route=route,
        date = timezone.now()
    )

def SuccessLog(user, title, description, route):
    Log.objects.create(
        user=user,
        level=2,
        title=title,
        description=description,
        route=route,
        date = timezone.now()
    )

def WarningLog(user, title, description, route):
    Log.objects.create(
        user=user,
        level=3,
        title=title,
        description=description,
        route=route,
        date = timezone.now()
    )

def ErrorLog(user, title, description, route):
    Log.objects.create(
        user=user,
        level=4,
        title=title,
        description=description,
        route=route,
        date = timezone.now()
    )

