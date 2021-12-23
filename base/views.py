from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    room_count = rooms.count()

    topics = Topic.objects.all()

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
    }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {
        'room': room,
    }
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {
        'obj': room,
    }
    return render(request, 'base/delete.html', context)


def loginpage(request):
    if request.method == 'POST': # get the user and the password
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if the user exist
        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exist')
        # if the user does not exist then check the credition are correct
        user = authenticate(request, username=username, password=password)
        # Log the user in
        if user is not None: 
            login(request, user) # create a session in the database
            return redirect('home')
        else: # if the user is not loggid in
            messages.error(request, 'User Or Password not exist')
            
    context = {}
    return render(request, 'base/login_register.html')


def logoutUser(request):
    logout(request)
    return redirect('home')