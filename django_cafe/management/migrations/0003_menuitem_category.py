# Generated by Django 5.1.6 on 2025-03-03 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_alter_menuitem_item_image_alter_menuitem_item_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='category',
            field=models.IntegerField(choices=[(0, 'Coffee'), (1, 'Tea'), (2, 'Cookies'), (3, 'Muffins'), (4, 'Cakes & Cupcakes'), (5, 'Pastries'), (6, 'Light Bites')], default=0),
        ),
    ]
