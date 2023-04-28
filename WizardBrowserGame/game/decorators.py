from django.utils import timezone
from .models import *

# Function to get turns to refresh
def getTurnsToRefresh(user):
    last_update = user.last_update
    last_update = last_update.replace(minute=0, second=0, microsecond=0)

    current_date = timezone.now()
    current_date = current_date.replace(minute=0, second=0, microsecond=0)

    diff = current_date - last_update
    hours = diff.total_seconds() / 3600 

    return int(hours)


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
                turnsToRefresh = getTurnsToRefresh(usuario)
                
                if turnsToRefresh > 0:
                    usuario.mana = usuario.mana + (usuario.level * turnsToRefresh)
                    usuario.last_update = timezone.now()
                    usuario.save()

        return refresh(request, usuario, *args, **kwargs)


    return RefreshResourcesFunc