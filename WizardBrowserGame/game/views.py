from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Decorator para refrescar el mana de los usuarios
#( poner: @RefreshResources encima de las vistas en las que se puedan recargar )
from game.decorators import RefreshResources 

# Create your views here.
def index(request, *args, **kwargs):
    context = {}
    return render(request, 'index/index.html', context)

def login(request):
    return render(request,"registration/login.html")

def logout(request):
    return render(request,"registration/logout.html")

@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('/accounts/password_change/done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "registration/changePassword.html", {
        'form': form
    })

def changePasswordDone(request):
    return render(request, "registration/changePasswordDone.html")


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

