# Generated by Django 5.2.2 on 2025-06-27 07:10

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
        ('tours', '0003_remove_tour_convert_ask_sell_remove_tour_insurance_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TourProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Tours On Sale',
                'verbose_name_plural': 'Tours On Sale',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tours.tour',),
        ),
        migrations.AlterField(
            model_name='sale',
            name='agent',
            field=models.ForeignKey(limit_choices_to={'is_active': True, 'is_staff': True, 'status': 'agent'}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sale',
            name='tour',
            field=models.ForeignKey(limit_choices_to={'end_sale__gte': datetime.date(2025, 6, 27), 'is_active': True, 'start_sale__lte': datetime.date(2025, 6, 27)}, on_delete=django.db.models.deletion.PROTECT, to='tours.tour'),
        ),
    ]
