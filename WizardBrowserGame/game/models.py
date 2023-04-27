from django.db import models

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