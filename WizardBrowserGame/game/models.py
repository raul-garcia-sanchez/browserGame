from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError

from django.utils import timezone


class User(AbstractUser):
    life = models.IntegerField(default=10)
    mana = models.IntegerField(default=10)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    last_update = models.DateTimeField(default=timezone.now, blank=True)
    def __str__(self):
        return self.username

class Log(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    log_level = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    route = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


class Action(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cost = models.IntegerField()
    # 1 Attack, 2 Defend, 3 Meditate
    action_type = models.IntegerField(        
        validators=[
            MaxValueValidator(3),
            MinValueValidator(1)
        ]
    )
    points = models.IntegerField()
    success_rate = models.IntegerField()
    exp_given = models.IntegerField()
    exp_extra = models.IntegerField(blank=True, null=True)
    action_img = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class StatisticsUser(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='idUser')
    act_date = models.DateField(auto_now_add=True)
    act_time = models.TimeField(auto_now_add=True)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="action")
    success_rate = models.IntegerField()
    actual_roll = models.IntegerField()
    success = models.BooleanField()
class EventHistory(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    user_transmitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transmitter')
    user_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    date = models.DateTimeField(auto_now_add=True)
    succeed = models.BooleanField()
    def __str__(self):
        return "{} {} to {}".format(self.user_transmitter, self.action.name, self.user_receiver)
    
class GameOption(models.Model):
    game_datetime_start = models.DateTimeField()
    game_datetime_end = models.DateTimeField()
    mins_between_turns = models.IntegerField()
    
    def save(self, *args, **kwargs):
        # asegurarse de que solo haya un objeto de Configuracion en la base de datos
        if not self.pk and GameOption.objects.exists():
            raise ValidationError('Solo se puede crear una instancia de Configuracion')
        return super().save(*args, **kwargs)