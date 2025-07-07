from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.common.models import Adult
from apps.sales.models import Customer
from apps.tours.models import Tour
from helpers.choices import SaleDiscountChoice


class Sale(models.Model):

    tour = models.ForeignKey(
        "tours.Tour",  on_delete=models.PROTECT,
        verbose_name='Tour Name'
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
    pick_up_time = models.TimeField(verbose_name="Pickup Time", null=True)
    area = models.CharField(verbose_name='Area', max_length=255, null=True)
    total_max = models.PositiveIntegerField(verbose_name='Total Max', default=0)
    region = models.ForeignKey(
        'common.Region',
        on_delete=models.PROTECT,
        null=True, blank=True,
    )
    hotel = models.ManyToManyField(
        'common.Hotel',
    )
    adult = models.ForeignKey(
        Adult,
        on_delete=models.PROTECT,
        null=True
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

    def tour_amount(self):
        extra_price = self.extra_prices.aggregate(
            amount=models.Sum('extra_price__price')
        )['amount'] or Decimal("0")

        age_price = self.age_prices.aggregate(
            amount=models.Sum('age_price__price')
        )['amount'] or Decimal("0")

        total = extra_price + age_price

        total_with_fee = total + (total * Decimal("0.015"))

        if self.discount_type == "percentage" and self.discount > 0:
            discounted = total_with_fee - (total_with_fee * (Decimal(self.discount) / Decimal("100")))
            return round(discounted, 2)
        else:
            return round(total_with_fee - Decimal(self.discount), 2)

    # @property
    # def tour_amount(self):
    #     extra_price = self.extra_prices.all().aggregate(
    #         amount=models.Sum('extra_price__price')
    #     )['amount'] or 0
    #     age_price = self.age_prices.all().aggregate(
    #         amount=models.Sum('age_price__price')
    #     )['amount'] or 0
    #
    #     total = extra_price + age_price
    #
    #     if self.discount_type == "percentage" and self.discount > 0:
    #         return round(total - (total * (Decimal(self.discount) / Decimal("100"))))
    #     else:
    #         return total - self.discount



class SaleAgePrice(models.Model):
    sale = models.ForeignKey(
        "sales.Sale",
        on_delete=models.PROTECT,
        related_name="age_prices",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
    )
    age_price = models.ForeignKey(
        'tours.TourAgePrice',
        on_delete=models.PROTECT,
    )



class SaleExtraPrice(models.Model):
    sale = models.ForeignKey(
        "sales.Sale",
        on_delete=models.PROTECT,
        related_name="extra_prices",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
    )
    extra_price = models.ForeignKey(
        'tours.TourExtraPrice',
        on_delete=models.PROTECT,
    )


class TourProxy(Tour):

    class Meta:
        proxy = True
        verbose_name = "Tours On Sale"
        verbose_name_plural = "Tours On Sale"
