import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from game.models import *
import random
from django.contrib.auth.hashers import make_password

fake = Faker(["es_CA", "es_ES"])


class Command(BaseCommand):

    def handle(self, *args, **options):

        usersEventHistory = []
        try:
            for i in range(200):
                username = fake.user_name()
                email = fake.email()
                first_name = fake.first_name()
                last_name = fake.last_name()
                password = "test"
                user, created = User.objects.get_or_create(
                    username=username, email=email)
                if created:
                    user.set_password(password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    if i < 5:
                        usersEventHistory.append(user)
        except:
            pass
        
        options = GameOption()
        options.game_datetime_start = timezone.now()
        options.game_datetime_end = timezone.now() + datetime.timedelta(days=30)
        options.mins_between_turns = 60
        options.save()

        userDemo, createdDemo = User.objects.get_or_create(
            username="brahian", email="brahianmonsalve412@gmail.com")
        if createdDemo:
            userDemo.set_password("test")
            userDemo.first_name = "Brahian"
            userDemo.last_name = "Monsalve"
            userDemo.save()

        userAdmin, createdAdmin = User.objects.get_or_create(
            username="admin", email="admin@gmail.com")
        if createdAdmin:
            userAdmin.set_password("admin123")
            userAdmin.first_name = "Raúl"
            userAdmin.last_name = "García"
            userAdmin.is_staff = True
            userAdmin.is_superuser = True
            userAdmin.save()

        ACTION_NAMES = [
            {
                "name": "Glacius",
                "description": "Raig de gel que causa un fred intens en l'objectiu debilitant-lo",
                "cost": 2,
                "action_type": 1,
                "points": 1,
                "success_rate": 90,
                "exp_given": 1,
                "exp_extra": 1,
                "action_img": "images/spell_images/Glacius.png"
            },
            {
                "name": "Confringo",
                "description": "Bola de foc que causa una gran explosió ardent en l'objectiu",
                "cost": 3,
                "action_type": 1,
                "points": 2,
                "success_rate": 80,
                "exp_given": 2,
                "exp_extra": 3,
                "action_img": "images/spell_images/Confringo.png"
            },
            {
                "name": "Crucio",
                "description": "Raig de energía verda maleïda que causa un dolor insuportable a l'objectiu",
                "cost": 5,
                "action_type": 1,
                "points": 5,
                "success_rate": 60,
                "exp_given": 3,
                "exp_extra": 0,
                "action_img": "images/spell_images/Crucio.png"
            },
            {
                "name": "Avada Kedavra",
                "description": "Maldició imperdonable que causa motísims danys a l'objectiu",
                "cost": 9,
                "action_type": 1,
                "points": 8,
                "success_rate": 20,
                "exp_given": 4,
                "exp_extra": 0,
                "action_img": "images/spell_images/Avada_Kedavra.png"
            },
            {
                "name": "Protego",
                "description": "Crea un escut protector que cura al usuari que la llença",
                "cost": 3,
                "action_type": 2,
                "points": 1,
                "success_rate": 100,
                "exp_given": 1,
                "exp_extra": 0,
                "action_img": "images/spell_images/Protego.png"
            },
            {
                "name": "Expecto Patronum",
                "description": "Llença un raig de llum que produeix una criatura que et curará en gran quantitat",
                "cost": 6,
                "action_type": 2,
                "points": 5,
                "success_rate": 40,
                "exp_given": 3,
                "exp_extra": 0,
                "action_img": "images/spell_images/Patronus.png"
            },
            {
                "name": "Aguamenti",
                "description": "Genera un doll d'aigua que crea un entorn relaxant i refrescant que genera experiència",
                "cost": 8,
                "action_type": 3,
                "points": 0,
                "success_rate": 60,
                "exp_given": 7,
                "exp_extra": 0,
                "action_img": "images/spell_images/Aguamenti.png"
            },
        ]

        for action in ACTION_NAMES:
            actionCreate = Action(
                name= action["name"],
                description= action["description"],
                cost= action["cost"],
                action_type= action["action_type"],
                points= action["points"],
                success_rate= action["success_rate"],
                exp_given= action["exp_given"],
                exp_extra= action["exp_extra"],
                action_img= action["action_img"]
            )

            actionCreate.save()

        users = User.objects.all()
        brahian = User.objects.get(username='brahian')
        actions = Action.objects.all()

        for i in usersEventHistory:
            user_transmitter = i
            action = fake.random_element(elements=actions)
            succeed = True
            event = EventHistory.objects.create(
                action=action, user_transmitter=user_transmitter, user_receiver=brahian, succeed=succeed)
            event.save()

        for i in range(5):
            user_transmitter = brahian
            action = fake.random_element(elements=actions)
            succeed = True
            event = EventHistory.objects.create(
                action=action, user_transmitter=user_transmitter, user_receiver=fake.random_element(elements=users), succeed=succeed)
            event.save()
