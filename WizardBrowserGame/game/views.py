from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}

    return render(request, 'index/index.html', context)

def cron(request):
    context = {}

    return render(request, 'index/cron.html', context)

def play_action(request):
    context = {}

    return render(request, 'index/play_action.html', context)

def messages(request):
    context = {}

    return render(request, 'index/messages.html', context)

def ranking(request):
    context = {}

    return render(request, 'index/ranking.html', context)
