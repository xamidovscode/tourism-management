from django.db import models
from django.core.exceptions import ValidationError

from apps import common
from apps.tours.models import Tour
from helpers.choices import SaleDiscountChoice


class Customer(models.Model):
    full_name = models.CharField(
        max_length=255
    )
    phone_number = models.CharField(
        max_length=255
    )
    age = models.IntegerField(
        default=0,
    )
    passport = models.CharField(
        max_length=255, null=True, blank=True
    )


    def __str__(self):
        return (
                self.full_name + " | " +
                str(self.phone_number[4:]) + " | age " +
                str(self.age) + " | " +
                str(self.passport if self.passport else "")
        )



class Sale(models.Model):

    tour = models.ForeignKey(
        "tours.Tour", on_delete=models.PROTECT,
    )
    age_prices = models.ManyToManyField(
        "tours.TourAgePrice",
    )
    extra_prices = models.ManyToManyField(
        "tours.TourExtraPrice",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateField(verbose_name="Tour Date")
    description = models.TextField(null=True, blank=True)
    agent = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.PROTECT,
        limit_choices_to={
            "is_staff": True,
            "status": "agent"
        }
    )
    region = models.ForeignKey(
        'common.Region',
        on_delete=models.PROTECT,
        null=True,
    )
    hotel = models.ManyToManyField(
        'common.Hotel',
    )
    customer = models.ManyToManyField(
        Customer,
    )
    discount = models.PositiveIntegerField(
        default=0,
    )
    discount_type = models.CharField(
        choices=SaleDiscountChoice.choices,
        default=SaleDiscountChoice.percentage,
    )

    def clean(self):

        if self.discount_type == SaleDiscountChoice.percentage and self.discount > 100:
            raise ValidationError("Discount percentage can not be greater than 100")

    class Meta:
        verbose_name = "My Sold Tours"
        verbose_name_plural = "My Sold Tours"


class TourProxy(Tour):

    class Meta:
        proxy = True
        verbose_name = "Tours On Sale"
        verbose_name_plural = "Tours On Sale"


class SaleHistoryProxy(Sale):

    class Meta:
        proxy = True
        verbose_name = "Sold Tours History"
        verbose_name_plural = "Sold Tours History"
