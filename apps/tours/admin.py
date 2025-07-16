from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.forms.models import BaseInlineFormSet

from apps.tours.models import *
from helpers.custom_admin import RestrictedAdmin


class TourAgePriceForm(forms.ModelForm):
    class Meta:
        model = TourAgePrice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        readonly_names = ['Adult', 'Child', 'Toddle']
        name_val = self.initial.get('name') or getattr(self.instance, 'name', None)

        if name_val in readonly_names:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['name'].widget.attrs['style'] = 'pointer-events: none; background-color: #f1f1f1;'


class TourAgePriceFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', [])
        if not initial:
            kwargs['initial'] = [
                {'name': 'Adult', 'min_age': 0, 'max_age': 1.99, 'price': 0},
                {'name': 'Toddle', 'min_age': 2, 'max_age': 5.99, 'price': 0},
                {'name': 'Child', 'min_age': 6, 'max_age': 11.99, 'price': 0},
            ]
        super().__init__(*args, **kwargs)


class TourAgeInline(admin.TabularInline):
    model = TourAgePrice
    form = TourAgePriceForm
    formset = TourAgePriceFormSet
    extra = 3

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj else 3


class TourExtraPriceInline(admin.TabularInline):
    model = TourExtraPrice
    extra = 1
    fields = ('name', 'adult_price', 'child_price', 'toddle_price', 'currency')



@admin.register(Tour)
class TourAdmin(RestrictedAdmin):
    inlines = (TourAgeInline, TourExtraPriceInline)

    list_display = (
        "id", 'name', 'is_pickup', "supplier", 'created',
        'type', 'hotel', 'concept', 'transfer_type', 'price_by_age'
    )

    list_display_links = (
        "id", 'name', 'is_pickup', "supplier", 'created',
        'type', 'hotel', 'concept', 'transfer_type', 'price_by_age'
    )

    list_filter = (
        "is_pickup", 'concept', 'type', 'transfer_type', "supplier",
    )

    search_fields = (
        "name", "id",
    )

    def price_by_age(self, obj):
        result = ""
        age_prices = TourAgePrice.objects.filter(tour=obj)

        for age_price in age_prices:
            currency = age_price.currency.name if age_price.currency else 'nomalum'
            result += f"{age_price.name} - {age_price.price} {currency}<br>"

        return format_html(result)

    price_by_age.short_description = "Prices By Age"
    price_by_age.admin_order_field = "id"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if not change:
            tour = form.instance
            default_prices = [
                {'name': 'Adult', 'min_age': 0, 'max_age': 1.99, 'price': 0},
                {'name': 'Toddle', 'min_age': 2, 'max_age': 5.99, 'price': 0},
                {'name': 'Child', 'min_age': 6, 'max_age': 11.99, 'price': 0},
            ]

            for data in default_prices:
                TourAgePrice.objects.get_or_create(
                    tour=tour,
                    name=data['name'],
                    defaults={
                        'min_age': data['min_age'],
                        'max_age': data['max_age'],
                        'price': data['price'],
                        'currency': None
                    }
                )



@admin.register(TourExtraPrice)
class TourExtraPriceAdmin(RestrictedAdmin):
    list_display = (
        "id", "tour", "name", "adult_price", "child_price", "toddle_price", "currency"
    )
    list_display_links = (
        "id", "tour", "name", "adult_price", "child_price", "toddle_price", "currency"
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