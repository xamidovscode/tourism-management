from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# admin.site.unregister(UserAdmin)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", 'full_name', 'username', 'is_staff', 'is_staff', )
    list_filter = ("id", 'full_name', 'username', 'is_staff', 'is_staff', )
