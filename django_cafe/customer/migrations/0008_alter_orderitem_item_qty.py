# Generated by Django 5.1.7 on 2025-03-10 07:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_alter_order_customer_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item_qty',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=10, message='Cannot place more than 10 of the same items!'), django.core.validators.MinValueValidator(limit_value=0, message='Invalid quantity provided')]),
        ),
    ]
