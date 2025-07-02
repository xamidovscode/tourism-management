import calendar
import json
from decimal import Decimal
from datetime import datetime

from django.contrib import admin
from django.http.response import JsonResponse

from helpers.custom_admin import RestrictedAdmin
from .models import *
from ..sales.models import Sale

admin.site.index_template = 'admin/customers/admin_index.html'
original_index = admin.site.index



def get_chart_data(month=None, year=None):
    today = datetime.today()
    year = year or today.year
    month = month or today.month

    days_in_month = calendar.monthrange(year, month)[1]

    labels = [str(day) for day in range(1, days_in_month + 1)]
    orders = [0] * days_in_month
    revenues = [0] * days_in_month
    total_prices = [0] * days_in_month

    sales = Sale.objects.filter(
        processed_at__year=year,
        processed_at__month=month
    )

    for day in range(1, days_in_month + 1):
        daily_sales = [s for s in sales if s.processed_at.day == day]
        orders[day - 1] = len(daily_sales)
        day_total = Decimal(0)
        for s in daily_sales:
            day_total += s.tour_amount
        revenues[day - 1] = float(day_total)
        total_prices[day - 1] = float(day_total)

    return {
        'labels': labels,
        'orders': orders,
        'revenues': revenues,
        'total_prices': total_prices,
    }

def custom_index(request, extra_context=None):
    extra_context = extra_context or {}

    selected_month = int(request.GET.get('month', datetime.today().month))
    selected_year = int(request.GET.get('year', datetime.today().year))

    chart_data = get_chart_data(month=selected_month, year=selected_year)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(chart_data)

    sales = Sale.objects.all()
    extra_context.update({
        'sales': sales,
        'chart_data': json.dumps(chart_data),
        'selected_month': selected_month,
        'selected_year': selected_year,
        'total_orders': sum(chart_data['orders']),
        'total_users': 1234,  # real ma'lumot bilan almashtiring
        'total_price_sum': sum(chart_data['total_prices']),
        'total_user_revenue': sum(chart_data['revenues']),
        'total_benefit_revenue': 1000.00,  # kerakli formulaga moslashtiring
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


