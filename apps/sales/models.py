from django.db import models

from apps.tours.models import Tour


class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name + " | " + str(self.phone_number[4:])



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
    processed_at = models.DateField()
    description = models.TextField(null=True, blank=True)
    agent = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.PROTECT,
        limit_choices_to={
            "is_staff": True,
            "status": "agent"
        }
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "My Sold Tours"
        verbose_name_plural = "My Sold Tours"


class TourProxy(Tour):
    class Meta:
        proxy = True
        verbose_name = "Tours On Sale"
        verbose_name_plural = "Tours On Sale"


class SaleProxy(Sale):
    class Meta:
        proxy = True
        verbose_name = "Sold Tours History"
        verbose_name_plural = "Sold Tours History"
