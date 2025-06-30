from .models import *
from rest_framework import serializers
from drf_base64.fields import Base64ImageField, Base64FileField


class UserSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False)
    old_password = serializers.CharField(write_only=True, required=False)
       
    def create(self, validated_data):
        password = validated_data.pop('password')

        validated_data['is_active'] = True
        validated_data['is_admin'] = False

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        old_password = validated_data.pop('old_password', None)

        if password is not None and not instance.check_password(old_password):
            raise serializers.ValidationError({'detail': 'Senha incorreta!'})
        if password is not None:
            instance.set_password(password)

        new_instance = super().update(instance, validated_data)
        return new_instance

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},
                        'old_password': {'write_only': True}}
        read_only_fields = ('id',)


        