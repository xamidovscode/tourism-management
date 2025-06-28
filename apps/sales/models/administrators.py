from apps.sales.models.agents import (
    Sale as BaseSale,
    SaleAgePrice as BaseSalesAgePrice,
    SaleExtraPrice as BaseSalesExtraPrice,
)


class SoldTours(BaseSale):

    class Meta:
        proxy = True
        verbose_name = "Sold Tours History"
        verbose_name_plural = "Sold Tours History"


class SoldToursAgePrice(BaseSalesAgePrice):

    class Meta:
        proxy = True
        verbose_name = "Sold Tours Age Price"
        verbose_name_plural = "Sold Tours Age Price"


class SoldToursExtraPrice(BaseSalesExtraPrice):

    class Meta:
        proxy = True
        verbose_name = "Sold Tours Extra Price"
        verbose_name_plural = "Sold Tours Extra Price"
