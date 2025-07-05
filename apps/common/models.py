from django.db import models
from django.utils.translation import gettext_lazy as _

class TourType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Tour Type Name"))

    class Meta:
        verbose_name = _("Tour Type")
        verbose_name_plural = _("Tour Types")

    def __str__(self):
        return self.name


class TransferType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Transfer Type Name"))

    class Meta:
        verbose_name = _("Transfer Type ")
        verbose_name_plural = _("Transfer Types ")

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Currency Name"))

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Hotel")
        verbose_name_plural = _("Hotels")

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Market")
        verbose_name_plural = _("Markets")

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class  Adult(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    min_age = models.FloatField(verbose_name=_("Minimum Age"))
    max_age = models.FloatField(verbose_name=_("Maximum Age"))

    def __str__(self):
        return f"{self.name} ({self.min_age}–{self.max_age} y)"


class  Child(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    min_age = models.FloatField(verbose_name=_("Minimum Age"))
    max_age = models.FloatField(verbose_name=_("Maximum Age"))

    def __str__(self):
        return f"{self.name} ({self.min_age}–{self.max_age} y)"

