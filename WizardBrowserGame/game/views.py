from django import forms
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied,BadRequest
from django.contrib.auth.hashers import make_password


from datetime import datetime
# Decorator para refrescar el mana de los usuarios
#( poner: @RefreshResources encima de las vistas en las que se puedan recargar )
from game.decorators import RefreshResources 

#Email imports
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

#Token imports
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes


def index(request, *args, **kwargs):
    return render(request, 'index/index.html')

def login(request):
    return render(request, "registration/login.html")

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

def passwordReset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = request.POST["email"]
            user = User.objects.get(email=user_email)

            if not user:
                return redirect("done/")
            else:
                #Funcion enviar email
                context = {}

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                confirmation_url = "http://localhost:8000/accounts/reset/" + uidb64 + "/" + token + "/"
                context = {'user':user, 'urlToGo':confirmation_url}

                template = get_template('mails/reset.html')
                content = template.render(context)

                email = EmailMultiAlternatives(
                    'Correu de recuperació de contrasenya',
                    "Confirmació de l'usuari: "+user.username,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                email.attach_alternative(content, 'text/html')
                email.send()
                return redirect("done/")
    else:
        form = PasswordResetForm()
    return render(request,"registration/passwordReset.html",{'form':form})

def passwordResetDone(request):
    return render(request,"registration/passwordResetDone.html")

def resetCheck(request,uidb64):
    error_msg = ""
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None:
        if request.method == "POST":
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            if (password and confirm_password and password == confirm_password):
                user.password = make_password(password)
                user.save()
                return render(request, 'registration/resetDone.html')

            else:
                error_msg = "Les contrasenyes han de coincidir"

        return render(request, 'registration/reset.html',{"error_msg":error_msg})

    raise BadRequest("Paràmetres no vàlids")

def resetDone(request):
    return render(request,"registration/resetDone.html")

def resetNotValid(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        return redirect("/accounts/reset/"+uidb64+"/set-password/")

    return render(request,"registration/resetNotValid.html")

def register(request):
    error_msg = ""
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            user_research_email = User.objects.filter(email=email)
            if user_research_email:
                error_msg = "Ja existeix un compte amb aquest email"
            else:
                user_research_username = User.objects.filter(username=username)

                if user_research_username:
                    error_msg = "Ja existeix un compte amb aquest nom d'usuari"
                else:
                    #Creacio de correu amb user not activated
                    new_user = User()
                    new_user.email = email
                    new_user.username = username
                    new_user.password = make_password(password)
                    new_user.is_active = False
                    new_user.save()

                    #ENVIAR CORREO DE VERIFICACION
                    context = {}

                    uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
                    token = default_token_generator.make_token(new_user)

                    confirmation_url = "http://localhost:8000/accounts/register/" + uidb64 + "/" + token + "/"
                    context = {'user':new_user, 'urlToGo':confirmation_url}

                    template = get_template('mails/register.html')
                    content = template.render(context)

                    email = EmailMultiAlternatives(
                        'Correu de confirmació de registre',
                        "Confirmació de l'usuari: "+new_user.username,
                        settings.EMAIL_HOST_USER,
                        [new_user.email]
                    )
                    email.attach_alternative(content, 'text/html')
                    email.send()
                    return redirect("emailSent/")

        else:
            error_msg = "Les contrasenyes han de coincidir"

    return render(request,"registration/register.html",{"error_msg":error_msg})

def registerSent(request):
    return render(request,"registration/registerSent.html")

def checkRegister(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/registerDone.html')

    raise BadRequest("Paràmetres no vàlids")

def registerDone(request):
    return render(request,"registration/registerDone.html")

@login_required
def changePasswordDone(request):
    return render(request, "registration/changePasswordDone.html")

def index(request):
    datesGame= GameOption.objects.get(pk=1)
    dateEnd = timezone.localtime(datesGame.game_datetime_end).timestamp()
    dateStart = timezone.localtime(datesGame.game_datetime_start).timestamp()
    dateNowTime = datetime.now().timestamp()
    dateNow =  datetime.now()
    print("dateNow -> ", dateNow)
    print("dateEnd -> ", dateEnd)
    print("dateNowTIme",dateNowTime)
    print("dateEnd mas pequeño que ahora -> ",dateEnd <= dateNowTime)
    minutesToTurn = 60 - dateNow.minute
    if(request.user.username):
        position = getPositionRankingUser(request.user)
        actions = actionsUser(request.user)
        return render(request, "game/index.html", {"position": position, "actions": actions})
    else:
        return render(request, "game/index.html", {"datesGame": datesGame, "minutesToTurn": minutesToTurn, "dateNow": dateNow, "dateEnd": dateEnd, "dateStart": dateStart, "dateNowTime": dateNowTime})

#RANKING USERS ORDER BY EXP
def getPositionRankingUser(user):
    ordered_users = User.objects.order_by('-level','-exp')
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

