from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from django.utils import timezone
from game.models import *
import random
from django.contrib.auth.hashers import make_password

fake = Faker(["es_CA","es_ES"])

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        usersEventHistory = []

        for i in range(200):
            username = fake.user_name()
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            password = "test"
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                if i < 5:
                    usersEventHistory.append(user)

        userDemo, createdDemo = User.objects.get_or_create(username="brahian", email="brahianmonsalve412@gmail.com")
        if createdDemo:
            userDemo.set_password("test")
            userDemo.first_name = "Brahian"
            userDemo.last_name = "Monsalve"
            userDemo.save()

        userAdmin, createdAdmin = User.objects.get_or_create(username="admin", email="admin@gmail.com")
        if createdAdmin:
            userAdmin.set_password("admin123")
            userAdmin.first_name = "Raúl"
            userAdmin.last_name = "García"
            userAdmin.is_staff = True
            userAdmin.is_superuser = True
            userAdmin.save()

        ACTION_NAMES = [
            'Agafeu electritzant',
            'Descàrrega de foc',
            'Il·lusió menor',
            'Impacte encertat',
            'Llums dansaires',
            'Llum',
            'Mà de mag',
            'Missatge',
            'Prestidigitació',
            'Raig de gebre',
            'Reparar',
            'Ruixada verinosa',
            'Esquitxada àcida',
            'Toc gelat'
                        ]

        for name in ACTION_NAMES:
            description = fake.sentence(nb_words=10)
            cost = random.randint(1, 10)
            action_type = random.randint(1, 3)
            points = random.randint(1, 10)
            success_rate = random.randint(1, 100)
            exp_given = random.randint(10, 50)
            exp_extra = random.randint(1, 20) if random.randint(0, 1) else None

            action = Action(
                name=name,
                description=description,
                cost=cost,
                action_type=action_type,
                points=points,
                success_rate=success_rate,
                exp_given=exp_given,
                exp_extra=exp_extra
            )

            action.save()

        users = User.objects.all()
        brahian = User.objects.get(username='brahian')
        actions = Action.objects.all()

        for i in usersEventHistory:
            user_transmitter = i
            action = fake.random_element(elements=actions)
            succeed = True
            event = EventHistory.objects.create(action=action, user_transmitter=user_transmitter, user_receiver=brahian, succeed=succeed)
            event.save()

        for i in range(5):
            user_transmitter = brahian
            action = fake.random_element(elements=actions)
            succeed = True
            event = EventHistory.objects.create(action=action, user_transmitter=user_transmitter, user_receiver=fake.random_element(elements=users), succeed=succeed)
            event.save()

