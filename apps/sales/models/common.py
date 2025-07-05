from django.db import models


class Customer(models.Model):
    full_name = models.CharField(
        max_length=255
    )
    phone_number = models.CharField(
        max_length=255
    )
    birth_date = models.DateField(verbose_name='Birth date', null=True, blank=True)
    passport = models.CharField(
        max_length=255, null=True, blank=True
    )


    def __str__(self):
        return (
                self.full_name + " | " +
                str(self.phone_number[4:]) + " | age " +
                str(self.birth_date) + " | " +
                str(self.passport if self.passport else "")
        )
