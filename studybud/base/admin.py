from django.contrib import admin
from .models import Room,Message,Topic,UserBio
# Register your models here.

admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(UserBio)
