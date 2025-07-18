# Generated by Django 5.2.2 on 2025-07-10 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0010_remove_tourageprice_max_age_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tourageprice',
            name='adult',
        ),
        migrations.AddField(
            model_name='tourageprice',
            name='max_age',
            field=models.FloatField(blank=True, null=True, verbose_name='Maximum Age'),
        ),
        migrations.AddField(
            model_name='tourageprice',
            name='min_age',
            field=models.FloatField(blank=True, null=True, verbose_name='Minimum Age'),
        ),
        migrations.AddField(
            model_name='tourageprice',
            name='name',
            field=models.CharField(default=1, max_length=100, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
