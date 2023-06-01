from django.db import models

# Create your models here.
class Chat(models.Model):
    text = models.CharField(max_length=100000000)
    created = models.DateField(auto_now_add=True)
    