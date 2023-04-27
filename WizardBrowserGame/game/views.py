from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}

    return render(request, 'index/index.html', context)

def login(request):
    return render(request,"registration/login.html")