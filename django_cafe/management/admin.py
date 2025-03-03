import csv
from django.http import HttpResponse
from django.contrib import admin
from . import models

@admin.action(description='Download CSV for selected')
def download_csv(model_admin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Menu Items.csv"'
    writer = csv.writer(response)

    headers = ['Item', 'Price', 'Rating']
    writer.writerow(headers)

    data = [[model.item_name, model.item_price, model.item_rating] for model in queryset]
    writer.writerows(data)

    return response


class MenuItemPriceFilter(admin.SimpleListFilter):
    title = 'Price Range Filter'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('0-50', '0-50 Rs'),
            ('50-100', '50-100 Rs'),
            ('100-200', '100-200 Rs'),
            ('200-500', '200-500 Rs'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == '0-50':
            return queryset.filter(item_price__lte=50)
        if self.value() == '50-100':
            return queryset.filter(item_price__range=(50, 100))
        if self.value() == '100-200':
            return queryset.filter(item_price__range=(100, 200))
        if self.value() == '500<=':
            return queryset.filter(item_price__gte=500)

admin.site.site_header = 'Admin Dashboard'

@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_price', 'item_rating')
    search_fields = ('item_name',)
    list_filter = (MenuItemPriceFilter,)
    actions=[download_csv]
    
    def has_add_permission(self, request):
        return request.user.is_staff