from django import forms
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied, BadRequest
from django.contrib.auth.hashers import make_password


from datetime import datetime
# Decorator para refrescar el mana de los usuarios
# ( poner: @RefreshResources encima de las vistas en las que se puedan recargar )
from game.decorators import RefreshResources

# Email imports
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

# Token imports
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def newLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                if user.is_staff:
                    SuccessLog(
                        user,
                        "Accés d'admin",
                        "Un compte d'administrador a accedit a la web mitjançant l'accés general",
                        "/accounts/login/"
                    )
                    return redirect("/admin")
                else:
                    SuccessLog(
                        user,
                        "Accés usuari",
                        "Un compte basic a accedit a la web",
                        "/accounts/login/"
                    )
                    return redirect("/")
        else:
            try:
                userActive = User.objects.get(
                    username=request.POST["username"])
                if userActive.is_active == False:
                    WarningLog(
                        userActive,
                        "Usuari no activat",
                        "Un compte basic a intentat accedir a la web sense tenir el compte activat",
                        "/accounts/login/"
                    )
                    form.errors.clear()
                    form.add_error(
                        None, "Has d'activar l'usuari per poder inciar sessió.")
            except:
                ErrorLog(
                    None,
                    "Intent d'accés",
                    "Algú ha intentat accedir a la web amb les següents credencials: Usuari=" +
                    request.POST["username"] + ", Contrasenya:" +
                    request.POST["password"],
                    "/accounts/login/"
                )
                form.errors.clear()
                form.add_error(
                    None, "Si us plau, introduïu un nom d'usuari i clau correctes. Observeu que ambdós camps poden ser sensibles a majúscules.")

    else:
        form = AuthenticationForm(request)
    return render(request, "registration/login.html", {'form': form})


@login_required
@RefreshResources
def logout(request):
    try:
        user = request.user
        SuccessLog(
            user,
            "Logout",
            "L'usuari ha fet logout",
            "/accounts/logout/"

        )
    except:
        ErrorLog(
            None,
            "Intent de sortida",
            "Algú ha fet logout sense haver accedit abans",
            "/accounts/logout/"
        )
    return render(request, "registration/logout.html")


@login_required
@RefreshResources
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            SuccessLog(
                request.user,
                "Canvi de contrasenya",
                "Usuari renova la seva contrasenya",
                "/accounts/password_change/"
            )
            return redirect('/accounts/password_change/done')
    else:
        form = PasswordChangeForm(request.user)
        InfoLog(
            request.user,
            "Entra a canvi de contrasenya",
            "Usuari entra a canvi de contrasenya",
            "/accounts/password_change/"
        )
    return render(request, "registration/changePassword.html", {
        'form': form
    })


def passwordReset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user_email = request.POST["email"]
                user = User.objects.get(email=user_email)

                if not user:
                    ErrorLog(
                        None,
                        "Recuperació de contrasenya",
                        "Email no trobat a la base de dades, email:"+user_email,
                        "/accounts/password_reset/"
                    )
                    return redirect("done/")
                else:
                    # Funcion enviar email
                    context = {}

                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)

                    confirmation_url = "http://localhost:8000/accounts/reset/" + uidb64 + "/" + token + "/"
                    context = {'user': user, 'urlToGo': confirmation_url}

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

                    SuccessLog(
                        user,
                        "Recuperació de contrasenya",
                        "Email enviat per a recuperar la contrasenya, email:"+user.email,
                        "/accounts/password_reset/"
                    )
                    return redirect("done/")
            except:
                ErrorLog(
                    None,
                    "Recuperació de contrasenya",
                    "Email no trobat a la base de dades, email:"+user_email,
                    "/accounts/password_reset/"
                )
                return redirect("done/")

    else:
        form = PasswordResetForm()
    return render(request, "registration/passwordReset.html", {'form': form})


def passwordResetDone(request):
    return render(request, "registration/passwordResetDone.html")


def resetCheck(request, uidb64):
    error_msg = []
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
                try:
                    validate_password(password)
                except ValidationError as error:
                    if error.messages:
                        for i in error.messages:
                            error_msg.append(i)
                else:
                    user.password = make_password(password)
                    user.save()
                    SuccessLog(
                        user,
                        "Restablir contrasenya",
                        "Usuari restableix la contrasenya",
                        "/accounts/reset/<uidb64>/set-password/"
                    )
                    return render(request, 'registration/resetDone.html')
            else:
                error_msg.append("Les contrasenyes han de coincidir")

        WarningLog(
            user,
            "Restablir contrasenya",
            "Usuari entra al link per restablir la contrasenya, errors:" +
            ",".join(error_msg),
            "/accounts/reset/<uidb64>/set-password/"
        )
        return render(request, 'registration/reset.html', {"error_msg": error_msg})

    raise BadRequest("Paràmetres no vàlids")


def resetDone(request):
    return render(request, "registration/resetDone.html")


def resetNotValid(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        return redirect("/accounts/reset/"+uidb64+"/set-password/")

    return render(request, "registration/resetNotValid.html")


def register(request):
    error_msg = []
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            try:
                validate_password(password)
            except ValidationError as error:
                if error.messages:
                    for i in error.messages:
                        error_msg.append(i)
            else:
                user_research_email = User.objects.filter(email=email)
                if user_research_email:
                    # error_msg = "Ja existeix un compte amb aquest email"
                    error_msg.append("Ja existeix un compte amb aquest email")
                else:
                    user_research_username = User.objects.filter(
                        username=username)

                    if user_research_username:
                        # error_msg = "Ja existeix un compte amb aquest nom d'usuari"
                        error_msg.append(
                            "Ja existeix un compte amb aquest nom d'usuari")
                    else:

                        # Creacio de correu amb user not activated
                        new_user = User()
                        new_user.email = email
                        new_user.username = username
                        new_user.password = make_password(password)
                        new_user.is_active = False
                        new_user.save()

                        # ENVIAR CORREO DE VERIFICACION
                        context = {}

                        uidb64 = urlsafe_base64_encode(
                            force_bytes(new_user.pk))
                        token = default_token_generator.make_token(new_user)

                        confirmation_url = "http://localhost:8000/accounts/register/" + \
                            uidb64 + "/" + token + "/"
                        context = {'user': new_user,
                                   'urlToGo': confirmation_url}

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
                        SuccessLog(
                            new_user,
                            "Usuari registrat",
                            "Nou usuari registrat, correu enviat per activar l'usuari, correu:"+new_user.email,
                            "/accounts/register/"
                        )
                        return redirect("emailSent/")

        else:
            # error_msg = "Les contrasenyes han de coincidir"
            error_msg.append("Les contrasenyes han de coincidir")

        WarningLog(
            None,
            "Registre d'usuari",
            "Usuari no registrat entra a registrar-se, errors:" +
            ",".join(error_msg),
            "/accounts/register/"
        )
    return render(request, "registration/register.html", {"error_msg": error_msg})


def registerSent(request):
    return render(request, "registration/registerSent.html")


def checkRegister(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        SuccessLog(
            user,
            "Usuari activat",
            "Nou usuari activat, ara pot fer login per accedir a la web",
            "/accounts/register/"
        )
        return render(request, 'registration/registerDone.html')

    raise BadRequest("Paràmetres no vàlids")


def registerDone(request):
    return render(request, "registration/registerDone.html")


@login_required
@RefreshResources
def changePasswordDone(request):
    return render(request, "registration/changePasswordDone.html")


@RefreshResources
def index(request):
    if request.user.is_staff:
        return redirect("/admin")
    datesGame = GameOption.objects.get(pk=1)
    dateEnd = timezone.localtime(datesGame.game_datetime_end).timestamp()
    dateStart = timezone.localtime(datesGame.game_datetime_start).timestamp()
    dateNowTime = datetime.now().timestamp()
    dateNow = datetime.now()
    minutesToTurn = 60 - dateNow.minute
    if (request.user.username):
        actions = actionsUser(request.user)
        InfoLog(
            request.user,
            "Usuari entra al perfil",
            "Usuari entra a veure el seu perfil i el temps pel següent torn",
            "/"
        )
        return render(request, "game/index.html", { "actions": actions})
    else:
        return render(request, "game/index.html", {"datesGame": datesGame, "minutesToTurn": minutesToTurn, "dateNow": dateNow, "dateEnd": dateEnd, "dateStart": dateStart, "dateNowTime": dateNowTime})

def actionsUser(user):
    actions_transmitted = EventHistory.objects.filter(
        user_transmitter=user, succeed=True)
    actions_received = EventHistory.objects.filter(
        user_receiver=user, succeed=True)
    history = list(actions_transmitted) + list(actions_received)
    ordered_history = sorted(
        history, key=lambda evento: evento.date, reverse=True)
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
    InfoLog(
        request.user,
        "Usuari entra al ranking",
        "Usuari entra a veure el ranking de tots els jugadors del joc",
        "/"
    )
    return render(request, 'game/ranking.html')

# Funcion logs
# Level 1:INFO, 2:SUCCESS , 3:WARNING, 4:ERROR


def InfoLog(user, title, description, route):
    Log.objects.create(
        user=user,
        log_level=1,
        title=title,
        description=description,
        route=route,
        date=timezone.now()
    )


def SuccessLog(user, title, description, route):
    Log.objects.create(
        user=user,
        log_level=2,
        title=title,
        description=description,
        route=route,
        date=timezone.now()
    )


def WarningLog(user, title, description, route):
    Log.objects.create(
        user=user,
        log_level=3,
        title=title,
        description=description,
        route=route,
        date=timezone.now()
    )


def ErrorLog(user, title, description, route):
    Log.objects.create(
        user=user,
        log_level=4,
        title=title,
        description=description,
        route=route,
        date=timezone.now()
    )
