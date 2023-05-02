from django.shortcuts import render
from .models import *
from django.utils import timezone
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

