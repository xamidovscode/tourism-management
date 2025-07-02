import json

from django.contrib import admin
from django.http.response import JsonResponse

from helpers.custom_admin import RestrictedAdmin
from .models import *

admin.site.index_template = 'admin/customers/admin_index.html'
original_index = admin.site.index


def get_chart_data(filters=None):
    # TODO: Add real data fetching based on filters
    # Example:
    labels = [str(i) for i in range(1, 31)]
    orders = [5, 10, 8, 12, 7, 9, 14, 6, 10, 11, 9, 7, 12, 15, 10, 9, 11, 13, 10, 8, 9, 7, 6, 11, 14, 10, 12, 9, 8, 7]
    revenues = [100, 200, 150, 300, 220, 180, 250, 190, 210, 240, 200, 180, 300, 320, 250, 210, 230, 260, 240, 190, 220, 180, 170, 230, 310, 260, 290, 220, 210, 180]
    total_prices = [120, 220, 180, 320, 240, 200, 270, 210, 230, 260, 220, 200, 320, 340, 270, 230, 250, 280, 260, 210, 240, 200, 190, 240, 320, 270, 300, 230, 220, 190]

    return {
        'labels': labels,
        'orders': orders,
        'revenues': revenues,
        'total_prices': total_prices,
    }

def custom_index(request, extra_context=None):
    extra_context = extra_context or {}

    # Assume fetching from DB or cache here
    chart_data = get_chart_data()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(chart_data)

    # Example static data - replace with real data counts
    extra_context.update({
        'categories': [],  # Provide real categories list from DB
        'user_levels': ["Gold", "Platinum", "Diamond"],
        'users': [],  # Provide real user list
        'chart_data': json.dumps(chart_data),
        'selected_month': 7,  # current month example
        'selected_year': 2025,
        'selected_category_id': '',
        'selected_user_type': '',
        'selected_user_id': '',
        'total_orders': sum(chart_data['orders']),
        'total_users': 1234,  # replace with real data
        'total_price_sum': sum(chart_data['total_prices']),
        'total_user_revenue': sum(chart_data['revenues']),
        'total_benefit_revenue': 1000.00,  # placeholder
    })

    return original_index(request, extra_context)

admin.site.index = custom_index


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


