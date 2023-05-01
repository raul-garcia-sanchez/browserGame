"""
URL configuration for WizardBrowserGame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from game.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('game.urls')),

    path("accounts/logout/", logout, name="logout"),
    path("accounts/password_change/", changePassword, name="changePassword"),

    path('accounts/password_reset/', passwordReset, name='password_reset'),
    path('accounts/password_reset/done/', passwordResetDone, name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', passwordResetDone, name='reset'),
    path('accounts/reset/done/', resetDone, name='reset_done'),

    path('accounts/register/', register, name='register'),
    path('accounts/register/done/', registerDone, name='register_done'),


    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)