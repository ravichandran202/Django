from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name="home"),
    path("login",views.loginPage, name="login"),
    path("register",views.registerPage, name="register"),
    path("logout",views.logoutUser, name="logout"),
    path("room/<str:pk>",views.room, name="room"),
    path("profile/<str:pk>",views.userProfile, name="user-profile"),
    path("profile/edit/<str:pk>",views.updateUser, name="updateuser"),
    path("createroom",views.createRoom, name="createroom"),
    path("updateroom/<int:pk>",views.updateRoom, name="updateroom"),
    path("deleteroom/<int:pk>",views.deleteRoom, name="deleteroom"),
    path("deletemessage/<int:pk>",views.deleteMessage, name="deletemessage"),
    path("topics",views.topicsPage, name="topics"),
    path("activity",views.activityPage, name="activity"),
]
