from django.http import JsonResponse
from .models import *

def getRanking(request):
    jsonData = list( User.objects.all().order_by('-level', '-exp', '-life').values() )
    for i, user in enumerate(jsonData):
        user["position"] = i + 1
    return JsonResponse({
            "status": "OK",
            "ranking": jsonData,
        }, safe=False)