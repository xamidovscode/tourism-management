# Generated by Django 5.2.2 on 2025-07-10 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_alter_adult_options'),
        ('sales', '0028_remove_sale_adult'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Adult',
        ),
    ]
