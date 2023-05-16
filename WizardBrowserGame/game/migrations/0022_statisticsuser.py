# Generated by Django 4.2 on 2023-05-13 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0021_delete_statisticsuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticsUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('success_rate', models.IntegerField()),
                ('actual_roll', models.IntegerField()),
                ('success', models.BooleanField()),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action', to='game.action')),
                ('idUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='idUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]