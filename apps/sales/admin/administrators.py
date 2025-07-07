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
        "id", "created_at", "tour", "processed_at", "agent", 'pick_up_time', 'description', 'export_buttons', 'area', 'adult', 'discount', 'total_max', 'discount_type'
    )
    list_display_links = (
        "id", "created_at", "tour", "processed_at", "agent", 'description', 'discount', 'discount_type'
    )
    list_filter = (
        "tour", "agent",
        ("processed_at", DateRangeFilter),
    )


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
