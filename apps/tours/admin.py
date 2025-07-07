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
            from apps.tours.models import Adult  # import qilib qo‘yamiz
            try:
                infant = Adult.objects.get(name__icontains='Infant')
                toddler = Adult.objects.get(name__icontains='Toodle')
                child = Adult.objects.get(name__icontains='Child')
            except Adult.DoesNotExist:
                kwargs['initial'] = []
                original_init(formset_self, *args, **kwargs)
                return

            kwargs['initial'] = [
                {'adult': infant, 'price': 0},
                {'adult': toddler, 'price': 0},
                {'adult': child, 'price': 0},
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
        "id", 'name', 'is_pickup', "supplier", 'created', 'type', 'hotel', 'concept', 'transfer_type', 'price_by_age'
    )
    list_display_links = (
        "id", 'name', 'is_pickup', "supplier", 'created', 'type', 'hotel', 'concept', 'transfer_type', 'price_by_age'
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
            if age_price.adult:
                name = age_price.adult.name
            else:
                name = "❌ (no category)"

            currency = age_price.currency.name if age_price.currency else "nomalum"

            result += f"{name} - {age_price.price} {currency}<br>"

        return format_html(result)

    price_by_age.short_description = "Prices By Age"
    price_by_age.admin_order_field = "id"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if not change:
            tour = form.instance
            from apps.tours.models import Adult

            default_names = ['Min infant Age', 'Min Toodle Age', 'Min Child Age']
            for name in default_names:
                try:
                    adult = Adult.objects.get(name=name)
                    TourAgePrice.objects.get_or_create(
                        tour=tour,
                        adult=adult,
                        defaults={'price': 0, 'currency': None}
                    )
                except Adult.DoesNotExist:
                    continue


@admin.register(TourExtraPrice)
class TourExtraPriceAdmin(RestrictedAdmin):
    list_display = ("id", "tour", "name", "price", "currency")
    list_display_links = ("id", "tour", "name", "price", "currency")
    list_filter = ("tour", "currency")


@admin.register(TourAgePrice)
class TourAgePriceAdmin(RestrictedAdmin):
    list_display = (
        "id", "tour", "get_name", "get_min_age", "get_max_age", "price", "currency"
    )
    list_display_links = (
        "id", "tour", "get_name", "get_min_age", "get_max_age", "price", "currency"
    )
    list_filter = ("tour", "currency")

    def get_name(self, obj):
        return obj.adult.name
    get_name.short_description = "Name"

    def get_min_age(self, obj):
        return obj.adult.min_age
    get_min_age.short_description = "Min Age"

    def get_max_age(self, obj):
        return obj.adult.max_age
    get_max_age.short_description = "Max Age"
