from django.shortcuts import render
from .models import Room


def home(request):
    return render(request, 'base/home.html')

def room(request):
    return render(request, 'base/room.html')
