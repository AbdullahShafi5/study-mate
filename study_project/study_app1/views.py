from pydoc_data.topics import topics
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Message, Room,Topic, User
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def LoginPage(request):
    page = 'login'
    user = None
    if request.user.is_authenticated:
        return redirect('home') #while you are logged in you are not allowing to  go to 'login/'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:  # user login system
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'WTF? user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password')
    context = {'page': page}
    return render(request, 'study_app1/login_registration.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request,'study_app1/login_registration.html',{'form':form})


def home(request):
    q = request.GET.get(
        'q') if request.GET.get('q') != None else ''  #wtf i did here? IDK
    rooms = Room.objects.filter(  #this is F**King annoying , but this field is for advanced search(sort of)__lol
        Q(topic__name__icontains=q) |  #if the query exist in topic
        Q(name__icontains=q) |  #if the query exist in title
        Q(description__icontains=q)  #if the query exist in description
    )
    topic = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q ))
    context = {'rooms_count': room_count, 
    'topic': topic,
    'rooms': rooms,
    'room_messages':room_messages,
    }

    return render(request, 'study_app1/home.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {
        'room': room,
        'room_messages':room_messages,
        'participants':participants,
        }
    return render(request, 'study_app1/room.html', context)


@login_required(login_url='/login')  #forcing user to login user
def create_room(request):
    form = RoomForm()  #this is for rendering form in the Html
    if request.method == 'POST':
        form = RoomForm(
            request.POST
        )  #and here we're taking the form input and saving the values to database

        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()            
            return redirect('home')

    context = {'form': form}
    return render(request, 'study_app1/room_form.html', context)

@login_required(login_url='/login')
def update_room(request, pk):  # updating my room
    room = Room.objects.get(id=pk)  #setting the room which we want to delete
    form = RoomForm(instance=room)
    if request.user != room.host :
        return HttpResponse('you are not allowed! so phak yo ')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'study_app1/room_form.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host :
        return HttpResponse('you are not allowed! so phak yo ')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'study_app1/delete.html', {'obj': room})


@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed! so phak yo ')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'study_app1/delete.html', {'obj': message})


def userProfile(request,pk):
    user= User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all() 
    context = {
        'user':user ,
        'rooms':rooms,        
        'room_messages':room_messages,
        'topics':topics,}
    return render(request, 'study_app1/profile.html', context)

