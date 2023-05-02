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

# Decorator para refrescar el mana de los usuarios
#( poner: @RefreshResources encima de las vistas en las que se puedan recargar )
from game.decorators import RefreshResources 
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
# EXAMPLE OF EMAIL
# email = EmailMessage(
#     'Asunto del correo electrónico', # Asunto
#     'Este es el cuerpo del correo electrónico.', # Cuerpo del correo electrónico
#     settings.EMAIL_HOST_USER, # E-mail del usuario
#     ['brahianmonsalve412@gmail.com'], # Lista de direcciones de correo electrónico de los destinatarios
# )
# email.send() #PARA ENVIAR EMAIL

def index(request, *args, **kwargs):
    context = {}
    print("********************************************************")
    user  = User.objects.get(pk=1)
    template = get_template('mails/register.html')
    context = {'user':user, 'urlToGo':'localhost:8000/register/done'}
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Correo test',
        'Test de registro',
        settings.EMAIL_HOST_USER,
        ['brahianmonsalve412@gmail.com']
    )
    email.attach_alternative(content, 'text/html')
    email.send()

    return render(request, 'index/index.html', context)

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
                #Funcion enviar emailget
                return redirect("done/")

            # print("User:",request.POST["email"])
            # form.save()
    else:
        form = PasswordResetForm()
    return render(request,"registration/passwordReset.html",{'form':form})

def passwordResetDone(request):
    return render(request,"registration/passwordResetDone.html")

def resetDone(request):
    return render(request,"registration/resetDone.html")

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
                    #ENVIAR CORREO DE VERIFICACION

                    # new_user = User()
                    # new_user.email = email
                    # new_user.username = username
                    # new_user.password = password
                    # new_user.save()
                    return redirect("done/")

        else:
            print("Passwords diferentes")
            error_msg = "Les contrasenyes han de coincidir"

    print("Error:",error_msg)
    return render(request,"registration/register.html",{"error_msg":error_msg})


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

