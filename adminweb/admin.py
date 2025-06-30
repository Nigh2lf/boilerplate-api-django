from django.contrib import admin
from .models import *


class MenuOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_menu', 'name', 'order', 'created_at')


admin.site.register(Config)
admin.site.register(MenuOption, MenuOptionAdmin)

