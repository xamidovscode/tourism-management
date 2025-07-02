from django.contrib import admin

from helpers.custom_admin import RestrictedAdmin
from ..models import *


@admin.register(Customer)
class CustomerAdmin(RestrictedAdmin):
    list_display = ('id', 'full_name', 'phone_number', "age", "passport")
    list_display_links = ('id', 'full_name', 'phone_number', "age", "passport")
    change_form_template = 'admin/customers/customer_detail.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        result = []
        customer = Customer.objects.get(pk=object_id)
        sales = Sale.objects.filter(description__icontains=customer.phone_number)

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
