from django.contrib import admin
from django.utils.html import format_html

from apps.tours.models import *
from helpers.custom_admin import RestrictedAdmin


class TourAgeInline(admin.TabularInline):
    model = TourAgePrice
    extra = 3

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj else 3

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj is None:
            formset.__init__ = self.wrap_init(formset.__init__)
        return formset

    def wrap_init(self, original_init):
        def new_init(formset_self, *args, **kwargs):
            kwargs['initial'] = [
                {'name': 'Min infant Age', 'min_age': 0, 'max_age': 1.99, 'price': 0},
                {'name': 'Min Toodle Age', 'min_age': 2, 'max_age': 5.99, 'price': 0},
                {'name': 'Min Child Age', 'min_age': 6, 'max_age': 11.99, 'price': 0},
            ]
            original_init(formset_self, *args, **kwargs)
        return new_init


class TourExtraPriceInline(admin.TabularInline):
    model = TourExtraPrice
    extra = 1


@admin.register(Tour)
class TourAdmin(RestrictedAdmin):
    inlines = (TourAgeInline, TourExtraPriceInline)
    list_display = (
        "id", 'name', 'is_pickup', "supplier", 'created', 'type', 'concept', 'transfer_type', 'price_by_age'
    )
    list_display_links = (
        "id", 'name', 'is_pickup', "supplier", 'created', 'type', 'concept', 'transfer_type', 'price_by_age'
    )
    list_filter = (
        "is_pickup", 'concept', 'type', 'transfer_type', "supplier",
    )
    search_fields = (
        "name", "id",
    )

    def price_by_age(self, obj):
        result = ""

        for age_price in TourAgePrice.objects.filter(tour=obj):
            result += str(str(age_price.name) + " - " + str(age_price.price) + f" {age_price.currency.name if age_price.currency else " nomalum"}" + "<br>")
        return format_html(result)

    price_by_age.short_description = "Prices By Age"
    price_by_age.admin_order_field = "agent"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if not change:
            tour = form.instance
            default_prices = [
                {'name': 'Min infant Age', 'min_age': 0, 'max_age': 1.99, 'price': 0},
                {'name': 'Min Toodle Age', 'min_age': 2, 'max_age': 5.99, 'price': 0},
                {'name': 'Min Child Age', 'min_age': 6, 'max_age': 11.99, 'price': 0},
            ]

            for data in default_prices:
                TourAgePrice.objects.get_or_create(
                    tour=tour,
                    name=data['name'],
                    defaults={
                        'min_age': data['min_age'],
                        'max_age': data['max_age'],
                        'price': data['price'],
                        'currency': None  # if needed
                    }
                )


@admin.register(TourExtraPrice)
class TourExtraPriceAdmin(RestrictedAdmin):
    list_display = (
        "id", "tour", "name", "price", "currency"
    )
    list_display_links = (
        "id", "tour", "name", "price", "currency"
    )

    list_filter = ("tour", "currency")


@admin.register(TourAgePrice)
class TourExtraPriceAdmin(RestrictedAdmin):
    list_display = (
        "id", "tour", "name", "min_age", "max_age", "price", "currency"
    )
    list_display_links = (
        "id", "tour", "name", "min_age", "max_age", "price", "currency"
    )
    list_filter = ("tour", "currency")




