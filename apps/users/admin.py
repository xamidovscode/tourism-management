from django.contrib import admin

from helpers.custom_admin import RestrictedAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(RestrictedAdmin):
    list_display = (
        "id", 'full_name', 'username', "created_at", 'status'
    )
    list_display_links = (
        "id", 'full_name', 'username', "created_at", 'status'
    )
    list_filter = (
        "id", 'status'
    )
    search_fields = (
        "full_name", 'username',
    )
    exclude = (
        "last_login",
        "date_joined",
        "is_staff",
        "is_active",
        'groups',
        'user_permissions',
        'is_superuser'

    )