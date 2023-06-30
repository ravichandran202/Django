from django.contrib import admin
from .models import TodoWork  #import TodoWork class from Models
# Register your models here.

#Register TodoWork model in admin.py file
admin.site.register(TodoWork)
