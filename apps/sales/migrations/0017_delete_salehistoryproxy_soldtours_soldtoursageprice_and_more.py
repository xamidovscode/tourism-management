# Generated by Django 5.2.2 on 2025-06-28 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0016_remove_sale_age_prices_remove_sale_customer_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SaleHistoryProxy',
        ),
        migrations.CreateModel(
            name='SoldTours',
            fields=[
            ],
            options={
                'verbose_name': 'Sold Tours History',
                'verbose_name_plural': 'Sold Tours History',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sales.sale',),
        ),
        migrations.CreateModel(
            name='SoldToursAgePrice',
            fields=[
            ],
            options={
                'verbose_name': 'Sold Tours Age Price',
                'verbose_name_plural': 'Sold Tours Age Price',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sales.saleageprice',),
        ),
        migrations.CreateModel(
            name='SoldToursExtraPrice',
            fields=[
            ],
            options={
                'verbose_name': 'Sold Tours Extra Price',
                'verbose_name_plural': 'Sold Tours Extra Price',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sales.saleextraprice',),
        ),
    ]
