from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models import Sum

from helpers.custom_admin import RestrictedAdmin
from .models import *

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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     for field_name in ['tour', 'agent', 'customer', 'region']:
    #         field = self.fields.get(field_name)
    #         if field and hasattr(field.widget, 'can_add_related'):
    #             field.widget.can_add_related = False
    #             field.widget.can_change_related = False
    #             field.widget.can_delete_related = False
    #             field.widget.can_view_related = False
    #
    #     for field_name in ['age_prices', 'extra_prices']:
    #         field = self.fields.get(field_name)
    #         if field and hasattr(field.widget, 'can_add_related'):
    #             field.widget.can_add_related = False
    #             field.widget.can_change_related = False
    #             field.widget.can_delete_related = False
    #             field.widget.can_view_related = False




@admin.register(Customer)
class CustomerAdmin(RestrictedAdmin):
    list_display = ('id', 'full_name', 'phone_number', "age", "passport")
    list_display_links = ('id', 'full_name', 'phone_number', "age", "passport")
    change_form_template = 'admin/customers/customer_detail.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        result = []
        sales = Sale.objects.filter(
            customer=object_id,
        )

        for sale in sales:
            result.append(
                [
                    str(sale.tour.name),
                    f"{sale.tour.start_sale} - {sale.tour.end_sale}",
                    str(sale.tour.transfer_type.name),
                    str(sale.agent.full_name),
                    str(sale.created_at.date()),
                ]
            )

        extra_context['default_table'] = result
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Sale)
class SaleAdmin(RestrictedAdmin):
    form = SaleForm

    list_display = (
        "id", "created_at", 'tour', 'processed_at', 'agent', 'tour_amount'
    )
    list_display_links = (
        "id", "created_at", 'tour', 'processed_at', 'agent', 'tour_amount'
    )
    list_filter = (
        "tour", "customer", "processed_at"
    )
    search_fields = (
        "tour__name",
    )
    exclude = ("agent", )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.agent = request.user
        obj.save()

    def tour_amount(self, obj):
        age_prices = obj.age_prices.all().aggregate(x=Sum('price'))['x'] or 0
        extra_prices = obj.extra_prices.all().aggregate(x=Sum("price"))['x'] or 0

        return f"{age_prices + extra_prices}"

        custom_field.short_description = "Price"
    tour_amount.admin_order_field = "agent"

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



@admin.register(SaleHistoryProxy)
class SaleProxyAdmin(RestrictedAdmin):
    list_display = (
        "id", "created_at", "tour", "processed_at", "agent", 'description', 'export_buttons', 'discount', 'discount_type'
    )
    list_display_links = (
        "id", "created_at", "tour", "processed_at", "agent", 'description', 'discount', 'discount_type'
    )
    list_filter = (
        "tour", "customer", "processed_at", "agent"
    )

    def export_buttons(self, obj):

        from django.utils.html import format_html
        from django.urls import reverse

        pdf_url = reverse('export_pdf', args=[obj.pk])
        excel_url = reverse('export_excel', args=[obj.pk])

        return format_html(
            '<a class="button" href="{}" title="Export PDF">🗂</a>&nbsp;'
            '<a class="button" href="{}" title="Export Excel">📊</a>',
            pdf_url, excel_url
        )

    export_buttons.short_description = "Export"
    export_buttons.admin_order_field = 'export_buttons'