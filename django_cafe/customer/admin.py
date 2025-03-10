from django.contrib import admin
from .models import Order, OrderItem
from django.contrib.auth.models import User

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','get_user_title', 'total_price', 'status', 'place_time', 'completed_time' ]
    search_fields = ['customer__username']

    def get_user_title(self, obj):
        if obj.customer:
            return obj.customer.username
        return "Offline Order"
    get_user_title.short_description = "Ordered By"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item_qty', 'item_total_price']
    # search_fields = ['order_instance__customer__username']
    def get_user_title(self, obj):
        return obj.order_instance.customer.username
    get_user_title.short_description = "Ordered by"
