__all__ = (
    "Tour",
    "TourAgePrice",
    "TourExtraPrice",
)

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TourType, TransferType, Currency, Hotel
from helpers.choices import (
    TourConceptChoice,
)


class Tour(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(_("Name"), max_length=100)
    is_pickup = models.BooleanField(_("Is Pickup"), default=False)
    supplier = models.BooleanField(_("Supplier"), default=False)
    concept = models.CharField(
        choices=TourConceptChoice, default=TourConceptChoice.STANDARD, verbose_name=_("Concept")
    )
    hotel = models.ForeignKey(Hotel, related_name="tours", on_delete=models.PROTECT)
    type = models.ForeignKey(TourType, verbose_name=_("Tour Type"), on_delete=models.PROTECT)
    allotment = models.PositiveIntegerField(_("Allotment(count)"), default=0)
    duration = models.IntegerField(_("Duration(days)"),default=0)
    transfer_type = models.ForeignKey(TransferType, verbose_name=_("Transfer Type"), on_delete=models.PROTECT)
    start_sale = models.DateField(_("Start Sale"))
    end_sale = models.DateField(_("End Sale"))

    def __str__(self):
        return self.name


class TourAgePrice(models.Model):
    tour = models.ForeignKey(Tour, verbose_name=_("Tour"), on_delete=models.PROTECT)
    name = models.CharField(_("Name"), max_length=100)
    min_age = models.FloatField(_("Minimum Age"), null=True, blank=True)
    max_age = models.FloatField(_("Maximum Age"), null=True, blank=True)
    price = models.DecimalField(_("Price"), max_digits=28, decimal_places=2, default=0)
    currency = models.ForeignKey(
        Currency, verbose_name=_("Currency"), on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return self.tour.name + " | " + str(self.min_age) + "-" + str(self.max_age) + " | " + str(self.price)


class TourExtraPrice(models.Model):
    tour = models.ForeignKey(Tour, verbose_name=_("Tour"), on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(_("Name"), max_length=255)
    price = models.DecimalField(_("Price"), max_digits=28, decimal_places=2, default=0)
    currency = models.ForeignKey(
        Currency, verbose_name=_("Currency"), on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return self.tour.name + " | " + self.name + " | " + str(self.price) + "-" + str(self.currency.name)





