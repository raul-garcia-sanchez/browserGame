from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint
from django.utils import timezone
from game.models import *

fake = Faker(["es_CA","es_ES"])

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        for i in range(200):
            username = fake.user_name()
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()