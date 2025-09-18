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

from django.apps import apps
from .models import *
from .serializers import *
from core.models import *
from core.serializers import *


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_admin(request):
    from rest_framework_simplejwt.tokens import RefreshToken

    if not 'email'in request.data:
        return Response({'detail': 'Falta o parâmetro username'}, status=status.HTTP_400_BAD_REQUEST)

    if not 'password'in request.data:
        return Response({'detail': 'Falta o parâmetro password'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email__iexact=request.data["email"], is_admin=True)

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
def get_user_and_menu(request):

    if request.user.is_admin == False:
        return Response({"detail": "Você não tem permissão para acessar este recurso!"}, status=status.HTTP_400_BAD_REQUEST)
    
    user_serializer = UserSerializer(request.user, many=False)

    menus = MenuOption.objects.filter(is_active=True).order_by('order')

    menu_serializer = MenuOptionSerializer(menus, many=True)

    return Response({
        "user": user_serializer.data,
        "menu": menu_serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_config(request):

    try:
        config = Config.objects.all().first()

    except Exception as e:
        return Response({"detail": "Erro ao obter configurações!"}, status=status.HTTP_400_BAD_REQUEST)
    
    config_serializer = ConfiSerializer(config, many=False)

    return Response(config_serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_config(request):

    if request.user.is_admin == False:
        return Response({"detail": "Você não tem permissão para acessar este recurso!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        config = Config.objects.all().first()

    except Exception as e:
        return Response({"detail": "Erro ao obter configurações!"}, status=status.HTTP_400_BAD_REQUEST)
    
    config_serializer = ConfiSerializer(config, data=request.data, partial=True)

    if config_serializer.is_valid():
        config_serializer.save()
        return Response(config_serializer.data)
    else:
        return Response(config_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_models(request):
    if request.user.is_admin == False:
        return Response({"detail": "Você não tem permissão para acessar este recurso!"}, status=status.HTTP_400_BAD_REQUEST)

    models = []
    label_apps = ['Token','TokenProxy','LogEntry','Permission','ContentType','Session','Group','Config','MenuOption']

    for model in apps.get_models():
        if model.__name__ not in label_apps:
            fields = []
            for field in model._meta.get_fields():
                # Apenas campos explícitos (não relacionamentos reversos ou campos auto-gerados)
                if hasattr(field, 'get_internal_type') and not field.many_to_many and not field.one_to_many and not field.one_to_one:
                    fields.append({
                        'name': field.name,
                        'type': field.get_internal_type()
                    })
            models.append({
                'model': model.__name__,
                'fields': fields
            })

    return Response(models)