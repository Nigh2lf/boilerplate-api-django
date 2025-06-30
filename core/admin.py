from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Register your models here.

admin.site.site_header = 'Projeto Admin'

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email',
                            'password',
                            'profile_image',
                            'name',
                            'is_deleted',
                            'is_active',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin) 
admin.site.unregister(DjangoGroup)


