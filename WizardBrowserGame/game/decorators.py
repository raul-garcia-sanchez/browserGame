from django.utils import timezone
from .models import *
from datetime import datetime, timedelta

# Function to get turns to refresh (every hour)


def getTurnsToRefresh(user):
    last_update = user.last_update
    last_update = last_update.replace(second=0, microsecond=0)

    current_date = timezone.now()
    current_date = current_date.replace(second=0, microsecond=0)

    diff = current_date - last_update
    secs_between_turns = (GameOption.objects.first().mins_between_turns) * 60

    turns = diff.total_seconds() // secs_between_turns
    resOfTurns = (diff.total_seconds() % secs_between_turns) * secs_between_turns # Diferencia de segundos perdida

    dateUserLastUpdate = current_date - timedelta(seconds=resOfTurns)

    return [int(turns),dateUserLastUpdate]


# Decorator to refresh resources
def RefreshResources(refresh):

    def RefreshResourcesFunc(request, *args, **kwargs):
        game_options = GameOption.objects.get(pk=1)
        start_date = game_options.game_datetime_start
        end_date = game_options.game_datetime_end
        current_date = timezone.now()

        if start_date <= current_date <= end_date:
            usuarios = User.objects.all()
            for usuario in usuarios:
                if (usuario.level > 0):
                    dataToRefresh = getTurnsToRefresh(usuario)
                    turnsToRefresh = dataToRefresh[0]
                    dateToSave = dataToRefresh[1]

                    if turnsToRefresh > 0:
                        maxMana = (usuario.level * 10)
                        if (maxMana > usuario.mana):

                            usuario.mana = usuario.mana + \
                                (usuario.level * turnsToRefresh)

                            if usuario.mana > maxMana:
                                usuario.mana = maxMana

                        usuario.last_update = dateToSave
                        usuario.save()

        return refresh(request, *args, **kwargs)

    return RefreshResourcesFunc
