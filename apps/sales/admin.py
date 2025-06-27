from django.contrib import admin

from .models import *

from django import forms
from django.contrib.admin.widgets import AdminDateWidget


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'processed_at': AdminDateWidget(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable "+" and "trash" icons for FK fields
        for field_name in ['tour', 'agent', 'customer']:
            field = self.fields.get(field_name)
            if field and hasattr(field.widget, 'can_add_related'):
                field.widget.can_add_related = False
                field.widget.can_change_related = False
                field.widget.can_delete_related = False

        # Disable "+" and "trash" for M2M fields
        for field_name in ['age_prices', 'extra_prices']:
            field = self.fields.get(field_name)
            if field and hasattr(field.widget, 'can_add_related'):
                field.widget.can_add_related = False
                field.widget.can_change_related = False
                field.widget.can_delete_related = False



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'phone_number',
    )
    list_display_links = (
        "id", 'full_name', 'phone_number',
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    form = SaleForm

    list_display = (
        "id", 'tour', 'processed_at', 'agent'
    )
    list_display_links = (
        "id", 'tour', 'processed_at', 'agent'
    )

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
class TourProxyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "is_pickup", "concept", "type", "allotment", "duration", "start_sale", "end_sale"
    )
    list_display_links = (
        "id", "name", "is_pickup", "concept", "type", "allotment", "duration", "start_sale", "end_sale"
    )
    list_filter = (
        "is_pickup", 'concept', 'type', 'transfer_type'
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False



@admin.register(SaleProxy)
class SaleProxyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "tour", "processed_at", "agent", 'description'
    )
    list_display_links = (
        "id", "tour", "processed_at", "agent", 'description'
    )