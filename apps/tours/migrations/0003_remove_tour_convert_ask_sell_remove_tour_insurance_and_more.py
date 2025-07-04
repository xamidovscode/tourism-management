# Generated by Django 5.2.2 on 2025-06-27 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0002_rename_tourage_tourageprice_tour_end_sale_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='convert_ask_sell',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='insurance',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='sale_status',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='status',
        ),
        migrations.AlterField(
            model_name='tour',
            name='allotment',
            field=models.PositiveIntegerField(default=0, verbose_name='Allotment'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='concept',
            field=models.CharField(choices=[('standard', 'Standard'), ('individual', 'Individual'), ('free', 'Free')], default='standard', verbose_name='Concept'),
        ),
    ]
