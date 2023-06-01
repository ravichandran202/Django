########################################
#
# Developer : Ravichandran T S
# Phone : 9113971166
# Email : ravichandrants202@gmail.com
#
########################################

from django.db import models
from django.contrib.auth.models import User

class TeamRegister(models.Model):
    team_name = models.CharField(max_length=100)
    team_size = models.IntegerField()
    college_name = models.CharField(max_length=100)
    person1 = models.CharField(max_length=100)
    person2 = models.CharField(max_length=100)
    person3 = models.CharField(max_length=100,blank=True)
    person4 = models.CharField(max_length=100,blank=True)
    leader_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    time = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    def __str__(self):
        return self.team_name
    
    
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.CharField(max_length=10000)
    
    def __str__(self):
        return self.name
    
    