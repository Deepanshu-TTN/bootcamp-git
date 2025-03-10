import csv
from django.http import HttpResponse
from django.contrib import admin
from . import models


admin.site.site_header = 'Admin Dashboard'


@admin.action(description='Download CSV for selected')
def download_csv(model_admin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Menu Items.csv"'
    writer = csv.writer(response)

    headers = ['Item', 'Price', 'Rating']
    writer.writerow(headers)

    data = [[model.name, model.price, model.rating] for model in queryset]
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
        

class MenuCategoryFilter(admin.SimpleListFilter):
    title='Filter by Categories'
    parameter_name='category'

    def lookups(self, request, model_admin):
        return (
            (0, 'Coffee'),
            (1, 'Tea'),
            (2, 'Cookies'),
            (3, 'Muffins'),
            (4, 'Cakes & Cupcakes'),
            (5, 'Pastries'),
            (6, 'Light Bites'),
        )
    
    def queryset(self, request, queryset):
        if self.value() is not None:
            category = int(self.value())
            return queryset.filter(category=category)
        return queryset
                


@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'rating')
    search_fields = ('name',)
    list_filter = (MenuItemPriceFilter, MenuCategoryFilter)
    actions=[download_csv]
    
    def has_add_permission(self, request):
        return request.user.is_staff