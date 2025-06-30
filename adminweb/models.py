from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from django.utils import timezone


class Config(models.Model):
    terms_of_use = models.TextField(null=True, blank=True)
    privacy_policy = models.TextField(null=True, blank=True)
    support_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


class MenuOption(models.Model):
    TYPE_MENU = (
        ('CONFIG', 'CONFIG'),
        ('CRUD', 'CRUD'),
        ('INSIDE WEB', 'INSIDE WEB'),
    )

    type_menu = models.CharField(max_length=255, null=True, blank=True, choices=TYPE_MENU)
    name = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    icon_web = models.TextField(null=True, blank=True)
    router_link = models.CharField(max_length=255, null=True, blank=True)
    config_url = models.CharField(max_length=255, null=True, blank=True)
    list_url = models.CharField(max_length=255, null=True, blank=True)
    get_by_id_url = models.CharField(max_length=255, null=True, blank=True)
    post_url = models.CharField(max_length=255, null=True, blank=True)
    patch_url = models.CharField(max_length=255, null=True, blank=True)
    delete_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 