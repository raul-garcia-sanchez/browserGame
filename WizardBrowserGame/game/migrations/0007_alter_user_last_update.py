# Generated by Django 4.2 on 2023-04-28 13:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_alter_user_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_update',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]