########################################
#
# Developer : Ravichandran T S
# Phone : 9113971166
# Email : ravichandrants202@gmail.com
#
########################################

from django.urls import path
from . import views

# urlpatterns = [
#     path('',views.index,name='index'),
#     path('signup',views.signup,name='signup'),
#     path('signin',views.signin,name='signin'),
#     path('register',views.register,name='register'),
#     path('TermsAndConditions',views.TermsAndConditions,name='TermsAndConditions'),
#     path('profile/edit',views.profileEdit,name='profileedit')
    
# ]

urlpatterns = [
    path("signup",views.signup,name="signup"),
    path("signin",views.signin,name="signin"),
    path("",views.index,name="index"),
    path("logout",views.logout,name="logout"),
    path('register',views.register,name='register'),
    path('payment/<int:id>',views.payment,name='payment'),
    path('payment',views.confirmpayment,name='confirmpayment'),
    path('termsandconditions',views.TermsAndConditions,name='TermsAndConditions'),
    path('profile/<int:id>',views.profile,name='profile'),
    
    #team operations
    path('teams', views.teamRecords, name='teams'),
    path('teams/edit/<int:id>', views.teamEdit, name='teamedit'),
    path('addteam', views.addteam, name='addteam'),
    path('teams/delete/<int:id>', views.teamDelete, name='teamdelete'),
    path('teams/edit/user/<int:id>', views.teamEditUser, name='teamedituser'),
    
    #user Records
    path('users', views.userRecords, name='users'),
]

