from django.contrib.admin import SimpleListFilter
from apps.tours.models import Tour


class VoucherNumberFilter(SimpleListFilter):
    title = 'Voucher Number'
    parameter_name = 'voucher_number'

    def lookups(self, request, model_admin):
        return [(tour.id, f"{tour.id}") for tour in Tour.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tour__id=self.value())

        return queryset