from django.contrib import admin
from . import models
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.site_header = 'Admin Dashboard'

@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_price', 'item_rating')


# Register your models here.
