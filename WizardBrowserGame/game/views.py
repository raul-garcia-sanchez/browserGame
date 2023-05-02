from django import forms
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied,BadRequest
from django.contrib.auth.hashers import make_password


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
    return render(request,"registration/login.html")

def logout(request):
    return render(request,"registration/logout.html")

#@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('change_password')
        #canviar mensajes de error
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
                    'Correu de confirmació de registre',
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
                        ['brahianmonsalve412@gmail.com']
                    )
                    email.attach_alternative(content, 'text/html')
                    email.send()
                    return redirect("done/")

        else:
            error_msg = "Les contrasenyes han de coincidir"

    return render(request,"registration/register.html",{"error_msg":error_msg})

def checkRegister(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.activated = True
        user.save()
        return render(request, 'registration/registerDone.html')

    raise BadRequest("Paràmetres no vàlids")

def registerDone(request):
    return render(request,"registration/registerDone.html")

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

