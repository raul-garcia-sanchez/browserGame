from django.db import models
from datetime import *
from django.contrib.auth.models import User

# Create your models here.

class Log(models.Model):

    def __str__(self):
        return self

class Opcions_Global(models.Model):
    
    def __str__(self):
        return self
    
class Accion(models.Model):
    
    def __str__(self):
        return self

class Event(models.Model):
    
    def __str__(self):
        return self

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.today)   

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'Perfiles de Usuario'