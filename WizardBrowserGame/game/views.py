from django.shortcuts import render

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
