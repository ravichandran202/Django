from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Creating our own model class with name TodoWork
class TodoWork(models.Model):
    #declaring attributes with respective data feilds
    user = models.ForeignKey(User,on_delete=models.CASCADE) #Foreignkey will referse the object of User Class
    work = models.TextField(max_length=1500)                #Used to store todo work information
    due_date = models.DateTimeField(null=True,blank=True)   #used to store Due_date 
    is_completed = models.BooleanField(default=False)       #used to store whether work is done or in progress
    is_due = models.BooleanField(default=False)             #used to determine whether the work is out of date
    created_at = models.DateTimeField(auto_now_add=True)    #created_at used to store the time in which object is created
    updated_at = models.DateTimeField(auto_now=True)        ##updated_at used to store the time in which object is corrected
    
    def __str__(self):
        return str(self.work)