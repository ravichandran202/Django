from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    phone = models.CharField(max_length=50,blank=True,null=True)
    role = models.CharField(max_length=50,blank=True,null=True)
    address = models.CharField(max_length=500,blank=True,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    

# Create your models here.
class Message(models.Model):
    content = models.TextField(max_length=100000)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sendto = models.ForeignKey(User,on_delete=models.CASCADE, related_name="sendto")
    isImage = models.BooleanField(default=False)
    imgURL = models.CharField(max_length=1000000, blank=True, null=True)
    msgtype = models.CharField(max_length=200,blank=True,null=True)
    
    def __str__(self):
        return self.content[:50]