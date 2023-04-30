from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Decorator para refrescar el mana de los usuarios
#( poner: @RefreshResources encima de las vistas en las que se puedan recargar )
from game.decorators import RefreshResources 

# Create your views here.
def index(request, *args, **kwargs):
    context = {}
    return render(request, 'game/index.html', context)

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

@login_required
def changePasswordDone(request):
    return render(request, "registration/changePasswordDone.html")

def dashboard(request):
    datesGame= GameOption.objects.get(pk=1)
    if(request.user.username):
        position = getPositionRankingUser(request.user)
        actions = actionsUser(request.user)
        return render(request, "game/dashboard.html", {"position": position, "actions": actions})
    else:
        return render(request, "game/dashboard.html", {"datesGame": datesGame})

#RANKING USERS ORDER BY EXP
def getPositionRankingUser(user):
    ordered_users = User.objects.order_by('-exp')
    position = list(ordered_users).index(user) + 1
    return position

def actionsUser(user):
    actions_transmitted = EventHistory.objects.filter(user_transmitter=user, succeed=True)
    actions_received = EventHistory.objects.filter(user_receiver=user, succeed=True)
    history = list(actions_transmitted) + list(actions_received)
    ordered_history = sorted(history, key=lambda evento: evento.date)
    return ordered_history
    

def cron(request):
    context = {}
    return render(request, 'game/cron.html', context)

def play_action(request):
    context = {}
    return render(request, 'game/play_action.html', context)

def messages(request):
    context = {}

    return render(request, 'game/messages.html', context)

def ranking(request):
    context = {}
    return render(request, 'game/ranking.html', context)

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

