from django.contrib import admin

from helpers.custom_admin import RestrictedAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(RestrictedAdmin):
    list_display = ("id", 'full_name', 'username', 'is_staff', 'is_staff', )
    list_filter = ("id", 'full_name', 'username', 'is_staff', 'is_staff', )
