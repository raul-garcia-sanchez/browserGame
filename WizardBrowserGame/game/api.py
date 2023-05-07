from django.http import JsonResponse
from .models import *
from django.db.models import Q


def getRanking(request):
    jsonData = list(User.objects.filter(is_staff=False, is_active=True).order_by(
        '-level', '-exp', '-life').values())
    for i, user in enumerate(jsonData):
        user["position"] = i + 1
    return JsonResponse({
        "status": "OK",
        "ranking": jsonData,
    }, safe=False)


def getCurrentUser(request):
    jsonData = list(User.objects.filter(pk=request.user.pk).values())

    if jsonData:
        return JsonResponse({
            "status": "OK",
            "user": jsonData,
        }, safe=False)
    else:
        return JsonResponse({
            "status": "OK",
            "user": "null",
        }, safe=False)


def getGameOptions(request):
    jsonData = list(GameOption.objects.all().values())
    return JsonResponse({
        "status": "OK",
        "gameOptions": jsonData
    }, safe=False)


def getActions(request):
    jsonData = list(EventHistory.objects.filter(
        Q(user_transmitter=request.user) | Q(user_receiver=request.user),
        succeed=True
    ).order_by('-date')[:25].select_related('user_transmitter').values('user_transmitter__username', 'action__name', 'user_receiver__username', 'date', 'succeed'))

    return JsonResponse({
        "status": "OK",
        "actions": jsonData
    });
