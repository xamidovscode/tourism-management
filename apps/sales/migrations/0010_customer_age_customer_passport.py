# Generated by Django 5.2.2 on 2025-06-28 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_remove_sale_customer_sale_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customer',
            name='passport',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
