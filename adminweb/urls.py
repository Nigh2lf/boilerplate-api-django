from webbrowser import get
from django.urls import path
from .views import *

urlpatterns = [

    #User:
    path('auth-admin/', auth_admin),
   
    #Get User and Menu:
    path('get-user-and-menu/', get_user_and_menu),

    #Config:
    path('get-config/', get_config),
    path('update-config/', update_config),
   
]