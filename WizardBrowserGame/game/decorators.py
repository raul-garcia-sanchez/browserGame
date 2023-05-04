from django.utils import timezone
from .models import *

# Function to get turns to refresh (every hour)
# def getTurnsToRefresh(user):
#     last_update = user.last_update
#     last_update = last_update.replace(minute=0, second=0, microsecond=0)

#     current_date = timezone.now()
#     current_date = current_date.replace(minute=0, second=0, microsecond=0)

#     diff = current_date - last_update
#     hours = diff.total_seconds() / 3600 

#     return int(hours)

# Function to get turns to refresh (every 2 mins) DONT USE IN PRODUCTION
def getTurnsToRefresh(user):
    last_update = user.last_update
    current_date = timezone.now()
    diff = current_date - last_update
    turns = diff.total_seconds() // 120
    return int(turns)



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
                    maxMana = (usuario.level * 10)

                    if (maxMana > usuario.mana):
                        turnsToRefresh = getTurnsToRefresh(usuario)

                        if turnsToRefresh > 0:
                            usuario.mana = usuario.mana + (usuario.level * turnsToRefresh)
                            
                            if usuario.mana > maxMana:
                                usuario.mana = maxMana

                            usuario.last_update = timezone.now()
                            usuario.save()

        return refresh(request, *args, **kwargs)


    return RefreshResourcesFunc