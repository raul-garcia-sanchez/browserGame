import json
import random
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


def getActions(request):
    jsonData = list(Action.objects.all().order_by("action_type").values())
    return JsonResponse({
        "status": "OK",
        "actions": jsonData,
        "status_code": 200
    }, safe=False)

def getEvents(request):
    jsonData = list(EventHistory.objects.filter(
        Q(user_transmitter=request.user) | Q(user_receiver=request.user),
        succeed=True
    ).order_by('-date')[:25].select_related('user_transmitter').values('user_transmitter__username', 'action__name', 'user_receiver__username', 'date', 'succeed'))

    return JsonResponse({
        "status": "OK",
        "actions": jsonData
    })

def getCurrentUser(request):
    jsonData = list(User.objects.filter(pk=request.user.pk).values())

    if jsonData:
        return JsonResponse({
            "status": "OK",
            "user": jsonData[0],
            "status_code": 200
        }, safe=False)
    else:
        return JsonResponse({
            "status": "OK",
            "user": None,
            "status_code": 404
        }, safe=False)


def makeAction(request):
    # Example of how post data should be:
    # {'action_id': 5, 'id_user_transmitter': 202, 'id_user_receiver': 202}
    if request.method == "POST":
        # data = json.loads(request.body)
        data = (request.body).decode('utf-8')
        eventDict = json.loads(data)
        try:
            hasKilled = False
            levelUp = False

            actionToMake = Action.objects.filter(id=eventDict["action_id"])[0]
            user_transmitter = User.objects.filter(
                id=eventDict["id_user_transmitter"])[0]
            user_receiver = User.objects.filter(
                id=eventDict["id_user_receiver"])[0]
            
            num_random = random.random()
            probabilities = actionToMake.success_rate / 100

            newEvent = EventHistory()
            newEvent.action = actionToMake
            newEvent.user_transmitter = user_transmitter
            newEvent.user_receiver = user_receiver
            newEvent.succeed = True

            # Reduction of mana
            if (user_transmitter.mana >= actionToMake.cost):
                user_transmitter.mana -= actionToMake.cost
                user_transmitter.exp += actionToMake.exp_given
            else:
                return JsonResponse({
                    "status": "OK",
                    "status_code": 400,
                    "error": "Not enough mana"
                }, safe=False)

            # If action failed
            if (num_random > probabilities):
                user_transmitter.exp -= actionToMake.exp_given # To mantain exp
                newEvent.succeed = False
                user_transmitter.save()
                newEvent.save()
                return JsonResponse({
                    "status": "OK",
                    "status_code": 200,
                    "action_succeed": False,
                }, safe=False)

            if (actionToMake.action_type == 1):
                user_receiver.life -= actionToMake.points # HP reduction of receiver
                user_transmitter.exp += actionToMake.exp_given # exp Gains of transmitter
                if (user_receiver.life <= 0): # If kills
                    hasKilled = True
                    user_receiver.level -= 1 # Level reduction of receiver
                    user_receiver.life = (10 * user_receiver.level)  # Reset HP of receiver
                    user_receiver.exp = 0   # Reset exp of receiver
                    user_transmitter.exp += actionToMake.exp_extra # Add exp_extra to transmitter
                    if (user_receiver.mana > (10 * user_receiver.level)):
                        # Reset mana if exceeds limits of level
                        user_receiver.mana = (10 * user_receiver.level)

                if (user_transmitter.exp >= (user_transmitter.level * 10)): # Check if levels up
                    levelUp = True
                    user_transmitter.exp = (user_transmitter.exp - (user_transmitter.level * 10)) 
                    user_transmitter.level += 1
                
                user_receiver.save()
                user_transmitter.save()


            elif (actionToMake.action_type == 2):
                user_transmitter.life += actionToMake.points # hp Gains of transmitter
                user_transmitter.exp += actionToMake.exp_given # exp Gains of transmitter

                if ( user_transmitter.life > (user_transmitter.level * 10) ): # Check if exceeds hp
                    user_transmitter.life = (user_transmitter.level * 10)
                
                if (user_transmitter.exp >= (user_transmitter.level * 10)): # Check if levels up
                    levelUp = True
                    user_transmitter.exp = (user_transmitter.exp - (user_transmitter.level * 10))
                    user_transmitter.level += 1

                user_transmitter.save()

            elif (actionToMake.action_type == 3):
                user_transmitter.exp += actionToMake.exp_given
                if (user_transmitter.exp >= (user_transmitter.level * 10)): # Check if levels up
                    levelUp = True
                    user_transmitter.exp = (user_transmitter.exp - (user_transmitter.level * 10))
                    user_transmitter.level += 1

                user_transmitter.save()
                

            newEvent.save()
            return JsonResponse({
                "status": "OK",
                "status_code": 200,
                "action_succeed": True,
                "has_killed": hasKilled,
                "levelUp": levelUp

            }, safe=False)
        
        except Exception as error:
            print("ERROR:", error)
            return JsonResponse({
                "status": "OK,exception",
                "status_code": 400,
                "error": "Exception thrown"
            }, safe=False)

    return JsonResponse({
        "status": "OK, notpost",
        "status_code": 400,
        "error": "Bad request"

    }, safe=False)

def getGameOptions(request):
    jsonData = list(GameOption.objects.all().values())
    return JsonResponse({
        "status": "OK",
        "gameOptions": jsonData
    }, safe=False)
