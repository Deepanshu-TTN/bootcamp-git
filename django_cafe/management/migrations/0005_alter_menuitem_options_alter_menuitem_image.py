# Generated by Django 5.1.7 on 2025-03-10 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_rename_item_description_menuitem_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitem',
            options={'permissions': [('can_delete_menuitems', 'Can Delete Menu Items')]},
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(default='images/png.webp', upload_to='images/'),
        ),
    ]
