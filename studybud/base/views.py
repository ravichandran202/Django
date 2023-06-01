from django.shortcuts import render,redirect
from .models import Room,Topic,Message,UserBio
from .forms import RoomForm,UserForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.

def registerPage(request):
    if request.method == 'POST':
        username = request.POST['username']    
        password1 = request.POST['password1']    
        password2 = request.POST['password2']    
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username Already Exists")
                return redirect("register")
            else:
                user = User(username=username,password=password1)
                user.save()
                auth.login(request,user)
                return redirect("home")
        else:
            messages.info(request,"Please Enter the same password")
            return redirect("register")
        
        
    return render(request,"base/login_register.html",{
        "login" : False,
        "form" : UserCreationForm
    })

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            messages.info(request,"User is not exists")
            return redirect("login")
    return render(request,"base/login_register.html",{
        "login" : True,
    })

def logoutUser(request):
    auth.logout(request)
    return redirect("home")

def home(request):
    
    q = request.GET['q'] if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(host__username__icontains = q)|
        Q(topic__name__icontains = q)|
        Q(name__icontains = q)|
        Q(description__icontains = q)
        )
    topics = Topic.objects.all()[:5]
    room_messages = Message.objects.all().order_by("-created").filter(
        Q(room__topic__name__icontains = q),
    )

    return render(request,"base/home.html",{
        "rooms" : rooms,
        "topics" : topics,
        "rooms_count" : rooms.count(),
        "room_messages":room_messages
    })

def room(request,pk):
    myroom = Room.objects.get(id=pk)
    message = myroom.message_set.all().order_by("-created")
    participants = myroom.participants.all()
    if request.method == 'POST':
        content = request.POST['comment']
        Message.objects.create(user=request.user,room=myroom,body = content)
        myroom.participants.add(request.user)
    
    return render(request,"base/room.html",{
        'room' : myroom,
        "messages" : message,
        "participants":participants
    })


def userProfile(request,pk):
    
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
     
    try:
        UserBio(host=User.objects.get(id=pk)).save()
    except:
        pass
    
    try:
        userbio = UserBio.objects.get(host=user)
    except:
        pass
    
    print(userbio.avatar)
    
    return render(request,"base/profile.html",{
        'user': user,
        'rooms':rooms,
        "room_messages" : room_messages,
        "topics":topics,
        'userbio': userbio
    })

@login_required(login_url="login")
def createRoom(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        topic_name = request.POST.get("topic")
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic = topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect("home")
    return render(request,"base/room_form.html",{
        "form":RoomForm,
        "topics":Topic.objects.all
    })

@login_required(login_url="login")
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse("You Are not allowed")
    
    if request.method == 'POST':
        topic_name = request.POST.get("topic")
        topic,created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        # if form.is_valid():
        #     form.save()
        return redirect("home")
    
    return render(request,"base/room_form.html",{
        "form":form,
        "topics":Topic.objects.all,
        "room":room
    })

@login_required(login_url="login")
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You Are not allowed")
    
    if request.method == "POST":
        room.delete()
        return redirect("home")
    
    return render(request,"base/delete.html",{
        "obj":room
    })
    
@login_required(login_url="login")
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You Are not allowed")
    
    if request.method == "POST":
        message.delete()
        return redirect("room",pk=message.room.id)
    
    return render(request,"base/delete.html",{
        "obj":message
    })

@login_required(login_url="login")
def updateUser(request,pk):
    user = request.user 
    form = UserForm(instance=user)
    userbio = UserBio.objects.get(host=user)
    
    
    if request.method == 'POST':
        # image = request.POST['avatar']
        bio = request.POST['bio']
        userbio = UserBio.objects.get(host=user)
        userbio.bio = bio
        userbio.save()
        
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request,"base/updateuser.html",{
        "form":form,
        "userbio":UserBio.objects.get(host=user)
    })
    
    
    
def topicsPage(request):
    q = request.GET['q'] if request.GET.get('q') != None else ''
    return render(request,'base/topics.html',{
        'topics':Topic.objects.filter(name__icontains=q)
    })
    
def activityPage(request):
    return render(request,'base/activity.html',{
    'room_messages':Message.objects.all()
    })