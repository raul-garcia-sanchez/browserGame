from django.http import JsonResponse
from .models import *


def getRanking(request):
    jsonData = list(User.objects.all().order_by(
        '-level', '-exp', '-life').values())
    return JsonResponse({
        "status": "OK",
        "ranking": jsonData,
    }, safe=False)


def getActions(request):
    jsonData = list(Action.objects.all().order_by("action_type").values())
    return JsonResponse({
        "status": "OK",
        "ranking": jsonData,
    }, safe=False)


def getCurrentUser(request):
    jsonData = list(User.objects.filter(pk=request.user.pk).values())

    if jsonData:
        return JsonResponse({
            "status": "OK",
            "ranking": jsonData,
        }, safe=False)
    else:
        return JsonResponse({
            "status": "OK",
            "ranking": "null",
        }, safe=False)
