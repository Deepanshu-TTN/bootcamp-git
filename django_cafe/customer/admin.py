from django.contrib import admin
from .models import Order, OrderItem
from django.contrib.auth.models import User

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['get_user_title', 'order_total_price', 'order_status', 'order_place_time', 'order_completed_time' ]
    search_fields = ['customer_id__username']

    def get_user_title(self, obj):
        return obj.customer_id.username
    get_user_title.short_description = "Ordered By"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'item_qty','get_user_title', 'order_instance', 'item_total_price']
    search_fields = ['order_instance__customer_id__username']
    def get_user_title(self, obj):
        return obj.order_instance.customer_id.username
    get_user_title.short_description = "Ordered By"


