# Generated by Django 4.2 on 2023-05-08 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_alter_gameoption_mins_between_turns'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='action_img',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
