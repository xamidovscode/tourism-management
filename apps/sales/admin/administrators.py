from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

from apps.tours.models import TourAgePrice
from helpers.custom_admin import RestrictedAdmin
from apps.sales.models import (
    SoldTours,
    SoldToursExtraPrice,
    SoldToursAgePrice
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
        "get_adult_price", "get_child_price", "get_toodle_price", 'discount', 'total_max', 'discount_type'
    )

    list_display_links = (
        "id", "created_at", "tour", "processed_at", "agent", 'pick_up_time', 'description', 'export_buttons', 'area',
        "get_adult_price", "get_child_price", "get_toodle_price", 'discount', 'total_max', 'discount_type'
    )
    list_filter = (
        "tour", "agent",
        ("processed_at", DateRangeFilter),
    )

    @staticmethod
    def get_price_by_name(obj, name):
        try:
            price_obj = TourAgePrice.objects.filter(tour=obj.tour, name=name).first()
            return f"{price_obj.price} {price_obj.currency.name}" if price_obj and price_obj.currency else price_obj.price
        except:
            return "-"

    def get_adult_price(self, obj):
        return self.get_price_by_name(obj, "Adult")

    def get_child_price(self, obj):
        return self.get_price_by_name(obj, "Child")
    def get_toodle_price(self, obj):
        return self.get_price_by_name(obj, "Toodle")

    get_adult_price.short_description = format_html('<span style="color: #1E90FF;">Adult</span>')
    get_child_price.short_description =  format_html("<span style='color: #1E90FF;'>Child</span>")
    get_toodle_price.short_description =  format_html("<span style='color: #1E90FF;'>Toodle</span>")


    def export_buttons(self, obj):
        pdf_url_1 = reverse('export_pdf1', args=[obj.pk])
        pdf_url_2 = reverse('export_pdf2', args=[obj.pk])
        excel_url = reverse('export_excel', args=[obj.pk])
        return format_html(
            '<div style="margin-bottom: 4px;">'
            '<a style="display:inline-block; white-space:nowrap; background:#e0f2e9; color:#2e7d32; padding:4px 8px; border-radius:4px; text-decoration:none;" '
            'href="{}" title="Export PDF 1">🗂 PDF 1</a>'
            '</div>'
            '<div style="margin-bottom: 4px;">'
            '<a style="display:inline-block; white-space:nowrap; background:#e3f2fd; color:#1565c0; padding:4px 8px; border-radius:4px; text-decoration:none;" '
            'href="{}" title="Export PDF 2">🗂 PDF 2</a>'
            '</div>'
            '<div>'
            '<a style="display:inline-block; white-space:nowrap; background:#fff3e0; color:#ef6c00; padding:4px 8px; border-radius:4px; text-decoration:none;" '
            'href="{}" title="Export Excel">📊 Excel</a>'
            '</div>',
            pdf_url_1, pdf_url_2, excel_url
        )

    export_buttons.short_description = "Export"
    export_buttons.admin_order_field = 'export_buttons'