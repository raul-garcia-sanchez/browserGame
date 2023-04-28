from django.shortcuts import *
# from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.middleware import csrf
from .forms import *
from .models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
# Create your views here.
def index(request):
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


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid(): 
            form.save()  # guardar el usuario en la base de datos si es válido
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Obtener el nombre de usuario
            user=User.objects.get(username=username)

            # Crear el perfil del usuario                                                                                                                                 
            new_profile = UserProfile(user=user, activation_key=activation_key, 
                key_expires=key_expires)
            new_profile.save()

            # Enviar un email de confirmación
            email_subject = 'Account confirmation'
            email_body = "Hola %s, Gracias por registrarte. Para activar tu cuenta da clíck en este link en menos de 48 horas: http://127.0.0.1:8000/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/accounts/register_success')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('user_profile/register.html', args, context_instance=RequestContext(request))

def register_confirm(request, activation_key):
    
    # Verifica que el usuario ya está logeado
    if request.user.is_authenticated():
        HttpResponseRedirect('/home')

    # Verifica que el token de activación sea válido y sino retorna un 404
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
    if user_profile.key_expires < timezone.now():
        return render_to_response('user_profile/confirm_expired.html')
    # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('user_profile/confirm.html')
