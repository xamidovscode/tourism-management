from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import models

from apps.sales.models import Customer
from apps.tours.models import Tour, TourAgePrice
from helpers.choices import SaleDiscountChoice


class Sale(models.Model):

    tour = models.ForeignKey(
        "tours.Tour",
        on_delete=models.PROTECT,
        related_name="sales",
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

    @property
    def base_price(self):
        """Fakat Adult + Child + Toodle narxlar yig'indisi (extra, discount yo'q)"""
        age_prices = TourAgePrice.objects.filter(
            tour=self.tour,
            name__in=["Adult", "Child", "Toodle"]
        )

        total = Decimal("0")
        for p in age_prices:
            total += p.price or Decimal("0")

        return total

    @property
    def service_fee(self):
        """1.5% servis to‘lovi faqat"""
        return (self.base_price * Decimal("0.015")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def total_amount(self):
        """Chegirma qo‘llangan yakuniy narx (base + service - discount)"""
        total = self.base_price + self.service_fee

        if self.discount_type == "percentage" and self.discount > 0:
            discount_amount = total * (Decimal(self.discount) / Decimal("100"))
        else:
            discount_amount = Decimal(self.discount)

        return (total - discount_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)



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
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('deactivate', 'Deactivate'),
    )

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
    sale_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Sale Status"
    )

class TourProxy(Tour):

    class Meta:
        proxy = True
        verbose_name = "Tours On Sale"
        verbose_name_plural = "Tours On Sale"
