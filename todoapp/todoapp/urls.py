from django.urls import path
from . import views

urlpatterns = [
    #set urls for our ToDo App
    path("",views.index,name="index"),
    path("logout",views.logout_user,name="logout"),
    path("signin",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path("delete/<int:id>",views.delete,name="delete"),
    path("complete/<int:id>",views.complete,name="complete"),
    path("edit/<int:id>",views.edit,name="edit"),
]
