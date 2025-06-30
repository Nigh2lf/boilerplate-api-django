from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
import json
from datetime import datetime, timedelta
from django.db.models import Q, Count, Sum
from rest_framework.response import Response
from .models import *
from .serializers import *
import urllib
from core.services_emails import *
import re


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_user(request):
    from rest_framework_simplejwt.tokens import RefreshToken

    if not 'email'in request.data:
        return Response({'detail': 'Falta o parâmetro username'}, status=status.HTTP_400_BAD_REQUEST)

    if not 'password'in request.data:
        return Response({'detail': 'Falta o parâmetro password'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email__iexact=request.data["email"], is_deleted=False)

    except Exception as e:
        return Response({"detail": "E-mail ou senha incorretos!"}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.is_active == True:

        if user.check_password(request.data["password"]):

            try:
                refresh = RefreshToken.for_user(user)

                update_last_login(None, user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"detail": "E-mail ou senha incorretos!"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"detail": "E-mail ou senha incorretos!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "E-mail ou senha incorretos!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):

    user = request.user

    user_serializer = UserSerializer(user).data

    return Response(user_serializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):

    if not 'email'in request.data:
        return Response({'detail': 'Does not have email'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=request.data["email"], is_active=True)

    except:
        return Response({'detail': 'E-mail não cadastrado!'}, status=status.HTTP_400_BAD_REQUEST)
    
    now = timezone.now()
    user.forgot_password_hash = re.sub(r"\D", "", str(now))
    user.forgot_password_expire = now + timedelta(hours=24)
    user.save()

    link = 'SITE/change-password/?email=%s&hash=%s' % (urllib.parse.quote(user.email), user.forgot_password_hash)

    send_email_forgot_password(user.email, user.name, link)

    return Response({'worked': True})


@api_view(['POST'])
@permission_classes([AllowAny])
def change_password_forgot_password(request):

    if not 'email'in request.data:
        return Response({'detail': 'Does not have email'}, status=status.HTTP_400_BAD_REQUEST)

    if not 'forgot_password_hash'in request.data:
        return Response({'detail': 'Does not have forgot_password_hash'}, status=status.HTTP_400_BAD_REQUEST)

    if not 'new_password'in request.data:
        return Response({'detail': 'Does not have new_password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=request.data["email"], forgot_password_hash=request.data["forgot_password_hash"])
    except:
        return Response({'detail': 'Erro get User and Hash'}, status=status.HTTP_400_BAD_REQUEST)

    now = timezone.now()

    if user.forgot_password_expire < now:
        return Response({'detail': 'Expire time forgot password'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(request.data["new_password"])
    user.forgot_password_expire = now
    user.save()

    return Response({'worked': True})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):

    user = request.user

    user.is_deleted = True
    user.is_active = False

    user.save()

    return Response({"detail": "Usuário deletado com sucesso!"})


