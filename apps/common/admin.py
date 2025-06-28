from django.contrib import admin
from . models import *

from helpers.custom_admin import RestrictedAdmin

@admin.register(TourType)
class TourTypeAdmin(RestrictedAdmin):
    list_display = ("id", "name")


@admin.register(TransferType)
class TourTypeAdmin(RestrictedAdmin):
    list_display = ("id", "name")


@admin.register(Currency)
class TourTypeAdmin(RestrictedAdmin):
    list_display = ("id", "name")


@admin.register(Hotel)
class TourTypeAdmin(RestrictedAdmin):
    list_display = ("id", "name")


@admin.register(Market)
class TourTypeAdmin(RestrictedAdmin):
    list_display = ("id", "name")


@admin.register(Region)
class RegionAdmin(RestrictedAdmin):
    list_display = ("id", "name")


