# Generated by Django 4.2 on 2023-04-28 13:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_action_alter_user_exp_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_update',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
