from django.shortcuts import render

def home(request):
    return render(request, 'home/index.html',{})

def equipo(request):
    return render(request, 'home/index.html',{})



