from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from django.utils import timezone
from core.models import User
from nameproject import settings


class Config(models.Model):
    terms_of_use = models.TextField(null=True, blank=True)
    privacy_policy = models.TextField(null=True, blank=True)
    support_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


# class MenuOption(models.Model):
#     TYPE_MENU = (
#         ('CONFIG', 'CONFIG'),
#         ('CRUD', 'CRUD'),
#         ('INSIDE WEB', 'INSIDE WEB'),
#     )

#     type_menu = models.CharField(max_length=255, null=True, blank=True, choices=TYPE_MENU)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     order = models.IntegerField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     icon_web = models.TextField(null=True, blank=True)
#     router_link = models.CharField(max_length=255, null=True, blank=True)
#     config_url = models.CharField(max_length=255, null=True, blank=True)
#     list_url = models.CharField(max_length=255, null=True, blank=True)
#     get_by_id_url = models.CharField(max_length=255, null=True, blank=True)
#     post_url = models.CharField(max_length=255, null=True, blank=True)
#     patch_url = models.CharField(max_length=255, null=True, blank=True)
#     delete_url = models.CharField(max_length=255, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
    
    
    
class CrudModelConfig(models.Model):
    TYPE_MENU = (
        ('CONFIG', 'CONFIG'),
        ('CRUD', 'CRUD'),
        ('INSIDE WEB', 'INSIDE WEB'),
        ('DASH', 'DASH'),
    )
    
    type_menu = models.CharField(max_length=255, null=True, blank=True, choices=TYPE_MENU)
    target_model = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150, blank=True, default="")
    url_name     = models.CharField(max_length=150, blank=True, default="")  # Ex: "products"

    icon = models.TextField(blank=True, default="")  
    
    enable_list   = models.BooleanField(default=True)
    enable_retrieve = models.BooleanField(default=True)
    enable_create = models.BooleanField(default=False)
    enable_update = models.BooleanField(default=False)
    enable_delete = models.BooleanField(default=False)

    default_ordering = models.CharField(max_length=120, blank=True, default="")
    search_fields    = models.JSONField(default=list, blank=True)   # ["name", "code",'is_deleted']
    
    # Auditoria simples
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CRUD Model Config"
        verbose_name_plural = "CRUD Model Configs"

    
class CrudFieldConfig(models.Model):
    model_config  = models.ForeignKey(CrudModelConfig, on_delete=models.CASCADE)
    field_name    = models.CharField(max_length=120)
    field_type    = models.CharField(max_length=80, blank=True, default="")  # ex: "CharField", 
    display_label = models.CharField(max_length=150, blank=True, default="")
    lookup_url    = models.CharField(max_length=150, blank=True, default="")  
    depends_on    =  models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    include_in_list   = models.BooleanField(default=False)
    include_in_retrieve = models.BooleanField(default=True)
    include_in_create = models.BooleanField(default=False)
    include_in_update = models.BooleanField(default=False)
    prefix = models.CharField(max_length=10, blank=True, default="")
    suffix = models.CharField(max_length=10, blank=True, default="")
    thousand_separator = models.CharField(max_length=10, blank=True, default="")
    decimal_marker = models.CharField(max_length=10, blank=True, default="")
    

    validators        = models.JSONField(default=list, blank=True)  # Ex: ["EmailValidator", "MaxLengthValidator"]
    
    required          = models.BooleanField(default=False)
    read_only         = models.BooleanField(default=False)

    order_index  = models.PositiveIntegerField(default=0)
    

    class Meta:
        unique_together = ("model_config", "field_name")
        ordering = ("order_index", "id")

class CrudFieldActionConfig(models.Model):
    field_config = models.ForeignKey(CrudFieldConfig, on_delete=models.CASCADE)
    action_name  = models.CharField(max_length=150, blank=True, default="")  
    action_type  = models.CharField(max_length=150, blank=True, default="")  
    parameters   = models.JSONField(default=dict, blank=True)  
    
    order_index  = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order_index", "id")    
    
#     Ação - 
#     Nome
#     EndPoint
#     Metodo
#     Extension
    
#     Retorno
#     caso arquivo RAW
#     caso json {
# Criar Padrão
# }
