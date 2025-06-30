from webbrowser import get
from django.urls import path
from .views_user import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [

    #User:
    path('auth-user/', auth_user),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('get-user/', get_user),
    path('forgot-password/', forgot_password),
    path('change-password-forgot-password/', change_password_forgot_password),
    path('delete-user/', delete_user),

    

]