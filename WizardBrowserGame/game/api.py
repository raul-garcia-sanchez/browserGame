from django.http import JsonResponse
from .models import *

def getRanking(request):
    jsonData = list( User.objects.filter(is_staff=False, is_active=True).order_by('-level', '-exp', '-life').values() )
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