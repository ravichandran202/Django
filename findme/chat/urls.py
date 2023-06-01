from django.urls import path
from . import views
urlpatterns = [
    path("",views.chat,name="chat"),
    path("delete/<str:id>",views.chatdelete,name="chatdelete")
]
