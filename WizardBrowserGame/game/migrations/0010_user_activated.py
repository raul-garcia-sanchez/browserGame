# Generated by Django 4.2 on 2023-05-02 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_gameoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
