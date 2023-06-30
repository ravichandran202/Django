#import required modules for our need
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,logout
from django.contrib import messages
from .models import TodoWork
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import datetime


#check if todo work is outdated or not
#if yes returns True else False
def check_due_date(due_date):
    if datetime.datetime.strptime(str(due_date)[:len(str(due_date))-6],"%Y-%m-%d %H:%M:%S") <= datetime.datetime.now():
        return True
    return False


#function to send email for the user who have created new todo item
def send_email(user,todo_work,due_date):
    subject = 'New Item Is Added'
    #write a message which is need to send
    message = f'Hi {user.username}, thank you for using TODO App.\nNew Item :{todo_work}\nDue_date : {due_date}\nis added into your TODO List.'
    html_content = f'''<h2>Hi, {user.username}, Thankyou for using TODO APP</h2><br>
                       <h4>New Item :  <p>{todo_work}</p></h4>
                       <h4>Due_date :  <p>{due_date}</p></h4><br><br><br>
                       
                       <p>Thankyou</p>
                       <p>Regards,</p>
                       <h4>TODO APP</h4> '''
    
    #set sender email address
    email_from = settings.EMAIL_HOST_USER
    
    #set reciever email address
    recipient_list = [user.email, ]
    try:
        msg = EmailMultiAlternatives(subject, message, email_from, recipient_list)
        #combaining HTML code into out email_sender 
        msg.attach_alternative(html_content,"text/html")
        msg.send()
    except:
        pass


#Create function to handle Registration Page
def signup(request):
    #Check if the request method is POST, and collect the data from the form
    if request.method == 'POST':
        #fetch the data
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        
        #check if the password and Re-entered passwords are same
        if password == confirm_password:
            #In order to maintain unique usernames, check if  the username is exists in our database
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists")
                return redirect("signup")
            else:
                #if all the conditions are true then save the requested user by using Usename and password
                user = User.objects.create_user(username,password = password,email=email).save()
                messages.info(request,"Registration Successful")
                return redirect("signin")
        else:
            messages.info(request,"Please enter same password")
            return redirect("signup")
            
    return render(request,'login_register.html',{  # initially we need to renderout the signup page
        'type' : 'signup'
    })

#Create function to handle Login Page
def signin(request):
    #Check if the request method is POST, and collect the data from the form
    if request.method == 'POST':
        #fetch the data
        username = request.POST['username']
        password = request.POST['password']
        #we are trying to check whether the user is exists in our database or not, and authenticate user using username,password
        user = authenticate(username = username, password=password)
        
        if user is not None:
            #if the authenticated user is exists then login into our app
            auth.login(request,user)
            return redirect("index")
        else:
            #if user trying to login with wrong details then alert him with message
            messages.info(request,'Username or Password is incorrect')
            return redirect("signin")    
    return render(request,'login_register.html',{
        'type' : 'signin'
    })
    
#Create function to handle logout request
def logout_user(request):
    logout(request)
    return redirect("signin")

#check if the user is loggedin ,if not redirect user into signin page
@login_required(login_url='signin')
#Create function to handle home page
def index(request):
    sort_type = ""
    filter_type = ""
    
    #filter out the lists that are present in the TodoWork models with only logedin user
    todoLists = TodoWork.objects.filter(user=request.user.id)
    #collect a data from the from using POST Method
    if request.method == 'POST':
        todo_work = request.POST['todo-work']
        due_date = str(request.POST['due-date'])
        TodoWork.objects.create(user=request.user,work=todo_work, due_date=due_date)
        
        send_email(request.user,todo_work,due_date)
        
    #Getting the data from the form using GET Requests 
    # Filtering and sorting the todo items as user request
    if request.method == 'GET':
        try:
            sort_type = request.GET['sort']
            filter_type = request.GET['filter']
        except:
            pass
        
        #checking the conditions to filter out the Data items
        if filter_type == "is_active":
            todoLists = TodoWork.objects.filter(Q(user=request.user.id) & Q(is_due=False) & Q(is_completed=False) ) #filter items based on Active 
        if filter_type == "is_completed":
            todoLists = TodoWork.objects.filter(Q(user=request.user.id) & Q(is_completed=True) ) #filter items based on completed 
        if filter_type == "is_due":
            todoLists = TodoWork.objects.filter(Q(user=request.user.id) & Q(is_completed=False) & Q(is_due=True)) #filter items based on dateout 
        
        #checking the contions to sortout the filtered items
        if sort_type == 'due_date':
            todoLists = todoLists.order_by('-due_date') #sort the items based on Due_date
        else:
            todoLists = todoLists[::-1]
        
    for list in todoLists: #iterate the filtered and sorted objects
        # set is_due feild as True if the certain objects are oudated
        if check_due_date(list.due_date) and not list.is_completed:
            list.is_due = True
            list.save()
        else :
            list.is_due = False
            list.save()
        
    return render(request,'todo.html',{
        'todoLists': todoLists
    })


@login_required(login_url='signin')
#handle the delete request for perticular items
def delete(request,id):
    TodoWork.objects.get(id=id).delete()
    return redirect('index')

@login_required(login_url='signin')
#set is_completed feild as True for perticular object
def complete(request,id):
    todo_msg = TodoWork.objects.get(id=id)
    todo_msg.is_completed = True
    todo_msg.save()
    return redirect('index')

@login_required(login_url='signin')
#user is allowed to edit todo_work feild
def edit(request,id):
    if request.method == 'POST':
        list_item = TodoWork.objects.get(id=id)
        list_item.work = request.POST['work']
        list_item.save()
        return redirect("index")
    return render(request,'edit.html',{
        'list' : TodoWork.objects.get(id=id)
    })