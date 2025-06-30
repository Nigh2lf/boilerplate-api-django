from .models import *
from rest_framework import serializers
from drf_base64.fields import Base64ImageField, Base64FileField


class ConfiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'
        read_only_fields = ('id',)


class MenuOptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MenuOption
        fields = ('id', 'type_menu', 'name', 'icon_web', 'router_link', 'config_url',)
        read_only_fields = ('id',)


class CompleteMenuOptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MenuOption
        fields = '__all__'
        read_only_fields = ('id',)