from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from helpers.custom_admin import RestrictedAdmin
from ..models import *

admin.site.disable_action('delete_selected')


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'processed_at': AdminDateWidget(attrs={'type': 'date'}),
        }

    class Media:
        js = ('admin/js/sale_filter.js',)

class SaleExtraPriceInline(admin.TabularInline):
    model = SaleExtraPrice
    extra = 0


class SaleAgePriceInline(admin.TabularInline):
    model = SaleAgePrice
    extra = 0


@admin.register(Sale)
class SaleAdmin(RestrictedAdmin):
    form = SaleForm

    inlines = (
        SaleAgePriceInline, SaleExtraPriceInline,
    )

    list_display = (
        "id", "created_at", 'tour', 'processed_at', 'agent', 'amount'
    )
    list_display_links = (
        "id", "created_at", 'tour', 'processed_at', 'agent', 'amount'
    )
    list_filter = (
        "tour", "processed_at"
    )
    search_fields = (
        "tour__name",
    )
    exclude = ("agent", )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.agent = request.user
        obj.save()

    def amount(self, obj):

        return obj.tour_amount

    amount.short_description = "Price"
    amount.admin_order_field = "tour_amount"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(agent=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name in ['tour', 'agent', 'customer']:
            field.widget.can_add_related = False
            field.widget.can_change_related = False
        return field

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        field = super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name in ['age_prices', 'extra_prices']:
            field.widget.can_add_related = False
            field.widget.can_change_related = False
        return field


@admin.register(TourProxy)
class TourProxyAdmin(RestrictedAdmin):
    list_display = (
        "id", "name", "is_pickup", "concept", "type", "allotment", "duration", "start_sale", "end_sale"
    )
    list_display_links = (
        "id", "name", "is_pickup", "concept", "type", "allotment", "duration", "start_sale", "end_sale"
    )
    list_filter = (
        "is_pickup", 'concept', 'type', 'transfer_type'
    )
    search_fields = ("name", )

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

