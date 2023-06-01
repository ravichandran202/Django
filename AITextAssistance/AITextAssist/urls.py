from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("chat",views.chat,name="chat"),
    path("profile/<str:id>",views.profile,name="profile"),    
    path("register",views.register,name="register"),    
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("delete/user/<str:id>",views.deleteUser,name="deleteUser"),   
]
