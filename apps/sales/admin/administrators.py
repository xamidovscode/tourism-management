from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

from apps.common.models import Adult
from helpers.custom_admin import RestrictedAdmin
from apps.sales.models import (
    SoldTours,
    SoldToursExtraPrice,
    SoldToursAgePrice, Sale
)


class SoldToursAgePriceInline(admin.TabularInline):
    model = SoldToursAgePrice
    extra = 0


class SoldToursExtraPriceInline(admin.TabularInline):
    model = SoldToursExtraPrice
    extra = 0


@admin.register(SoldTours)
class SaleProxyAdmin(RestrictedAdmin):
    inlines = (SoldToursAgePriceInline, SoldToursExtraPriceInline)

    list_display = (
        "id", "created_at", "tour", "processed_at", "agent", 'pick_up_time', 'description', 'export_buttons', 'area',
        'get_adult1', 'get_adult2', 'get_adult3', 'discount', 'total_max', 'discount_type'
    )
    llist_display_links = (
    "id", "created_at", "tour", "processed_at", "agent",
    'description', 'discount', 'discount_type',
    'get_adult1', 'get_adult2', 'get_adult3'
)
    list_filter = (
        "tour", "agent",
        ("processed_at", DateRangeFilter),
    )

    def get_adult1(self, obj):
        return " "

    def get_adult2(self, obj):
        return " "

    def get_adult3(self, obj):
        return " "

    @staticmethod
    def take_first_adult():
        adults = Adult.objects.first()
        return adults if adults else "N/A"

    @staticmethod
    def take_2_adult():
        adults = Adult.objects.all()
        if not adults:
            return "N/A"
        return adults[1] if adults.exists() else "N/A"

    @staticmethod
    def take_3_adult():
        adults = Adult.objects.all()
        if not adults:
            return "N/A"
        return adults[2] if adults.exists() else "N/A"

    get_adult1.short_description = format_html('<span style="color: #1E90FF;">{}</span>', take_first_adult.__func__())
    get_adult2.short_description = format_html('<span style="color: #1E90FF;">{}</span>', take_2_adult.__func__())
    get_adult3.short_description = format_html('<span style="color: #1E90FF;">{}</span>', take_3_adult.__func__())

    def export_buttons(self, obj):
        pdf_url = reverse('export_pdf', args=[obj.pk])
        excel_url = reverse('export_excel', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" title="Export PDF">🗂 PDF</a>&nbsp;'
            '<a class="button" href="{}" title="Export Excel">📊 Excel</a>',
            pdf_url, excel_url
        )

    export_buttons.short_description = "Export"
    export_buttons.admin_order_field = 'export_buttons'
