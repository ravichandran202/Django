from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import Message,UserInfo
from django.contrib.auth.decorators import login_required
import requests

def AIChatResponse(message):
    try:
        url = "https://lemurbot.p.rapidapi.com/chat"
        payload = {
        	"bot": "dilly",
        	"client": "d531e3bd-b6c3-4f3f-bb58-a6632cbed5e2",
        	"message": str(message)
        }
        headers = {
        	"content-type": "application/json",
        	"X-RapidAPI-Key": "65ad8e523fmshe2887d22f78c6a6p11a1ebjsnca2cd0a010af",
        	"X-RapidAPI-Host": "lemurbot.p.rapidapi.com"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()['data']['conversation']['output']
    except:
        return "Something goes wrong..."


def AITranslateResponse(message,translate_to = 'kn'):
    try:
        url = "https://text-translator2.p.rapidapi.com/translate"
        
        payload = {
        	"source_language": "en",
        	"target_language": translate_to,
        	"text": message
        }
        headers = {
        	"content-type": "application/x-www-form-urlencoded",
        	"X-RapidAPI-Key": "65ad8e523fmshe2887d22f78c6a6p11a1ebjsnca2cd0a010af",
        	"X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
        }
        
        response = requests.post(url, data=payload, headers=headers)
        
        return str(response.json()['data']['translatedText'])
    except:
        return "Something goes wrong..."


def AIImageResponse(imageRequestName):
    try:
        url = "https://texttoimage.p.rapidapi.com/image"
        
        payload = {
        	"search_text": imageRequestName,
        	"num_images": 1,
        	"pro_blog": True
        }
        headers = {
        	"content-type": "application/json",
        	"X-RapidAPI-Key": "65ad8e523fmshe2887d22f78c6a6p11a1ebjsnca2cd0a010af",
        	"X-RapidAPI-Host": "texttoimage.p.rapidapi.com"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        imagelink = response.json()['body']['images'][0]['link']
        
        imageObject = {}
        imageObject['caption'] = str(imageRequestName)
        imageObject['url'] = str(imagelink)
        return imageObject
    except:
        return "Something goes wrong..."

def verifyLength(message):
    message_list = []
    count = 0
    formatted_msg = ''
    if len(message) > 20:
        message_list = message.split()
        for word in message_list:
            if count%10 == 0:
                formatted_msg += word + "\n"
            else:
                formatted_msg += word + " "
            count += 1
    return formatted_msg
            
# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists")
                return redirect("register")
            else:
                user = User.objects.create_user(username,password = password1).save()
                messages.info(request,"Registration Successful")
                return redirect("register")
        else:
            messages.info(request,"Please enter same password")
            return redirect("register")
    return render(request,"base/login_register.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect("index")
        else:
            messages.info(request,'Username or Password is incorrect')
            return redirect("register")    
    return render(request,"base/login_register.html")

def logout(request):
    auth.logout(request)
    return redirect("index")


def index(request):
    try:
        AImessages = []
        MYmessages = []
        aimessages = Message.objects.all().order_by("-created")[:8:2]
        mymessages = Message.objects.all().order_by("-created")[1:8:2]
        messages = []
        for message in aimessages:
            AImessages.append(message.content)
        for message in mymessages:
            MYmessages.append(message.content)
        
        for i in range(len(AImessages)):
            dictionary = {}
            dictionary['answer'] = AImessages[i]
            dictionary['question'] = MYmessages[i]
            messages.append(dictionary)
    except:
        pass        
    
    return render(request,"base/index.html",{
        "messages":messages
    })

@login_required(login_url='login')
def chat(request):
    try:
        messages = Message.objects.all()
        AIUser = User.objects.get(username = "openai")
        
        if request.method == 'POST':
            content = request.POST['content']
            operation_type = request.POST['operation-type']
            
    
            if(operation_type=="chat"):                                           #Chat Bot Operation
                Message(content=content,user=request.user,sendto= AIUser).save()
                AIResponse_msg = AIChatResponse(content)
                Message(content=AIResponse_msg,user= AIUser,sendto = request.user,msgtype='chat').save()
                
            if(operation_type == "image"):
                Message(content=content,user=request.user,sendto = AIUser).save()
                AIResponse_msg = AIImageResponse(content)
                Message(content="Image : "+AIResponse_msg["caption"],user=AIUser,sendto = request.user,isImage=True,imgURL=AIResponse_msg["url"],msgtype='image').save()
                
            if(operation_type!="chat" and operation_type!="image"):                                          # Translate Language
                Message(content= "Translate : ' " + content + " ' to " + operation_type,user=request.user,sendto=AIUser).save()
                
                # AIResponse_msg = AIChatResponse(content)
                # AIResponse_msg = AITranslateResponse(AIResponse_msg,operation_type)
                
                AIResponse_msg = AITranslateResponse(content,operation_type)
                Message(content=AIResponse_msg,user= AIUser,sendto = request.user,msgtype='translate').save()
            
            # print(AIResponse_msg)
            # if(operation_type!="image"):
            #     Message(content=AIResponse_msg,user= AIUser,sendto = request.user).save()
    except:
        pass
    return render(request,"base/chat_page.html",{
        "messages" : messages,
    })


@login_required(login_url='login')
def profile(request,id):
    user = User.objects.get(id=id)
    
    messages = Message.objects.filter(user=User.objects.get(username='openai'))
    
    APIRequest = {
        "chat" : 0,
        "translate" : 0,
        "image" : 0,
        "total" : 0
    }
    
    for message in messages:
        if message.sendto == request.user:
            if message.msgtype == 'translate':
                APIRequest['translate'] += 1
            if message.msgtype == 'chat':
                APIRequest['chat'] += 1
            if message.msgtype == 'image':
                APIRequest["image"] += 1
    APIRequest['total'] = APIRequest['chat']+APIRequest["translate"]+APIRequest['image']


    global userinfo
    try:
        userinfo = UserInfo.objects.get(user_id=user.id)
    except:
        userinfo = UserInfo(user_id=request.user.id).save()
    
    if request.method == 'POST':
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email = request    .POST['email']
        userinfo.phone = request.POST['phone']
        userinfo.address = request.POST['address']
        userinfo.role = request.POST['role']
        user.save()
        userinfo.save()
 
    return render(request,"base/profile.html",{
        "user":user,
        "userinfo":userinfo,
        "APIRequest":APIRequest,
    })
    
@login_required(login_url='login')
def deleteUser(request,id):
    if request.method == 'POST':
        request.user.delete()
        return redirect("login")
    
    return render(request,"base/deleteUser.html")
    
# @login_required(login_url='login')
# def deleteMsg(request,id):
#     if request.method == 'POST':
#         redirect("login")
#         request.user.delete()
    
#     return render(request,"base/deleteUser.html",{
#         "object" : request.user.username
#     })