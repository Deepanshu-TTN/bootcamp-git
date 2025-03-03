from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage, name='manage'),
    path('additem/', views.create_menu_item, name='additem'),
    path('remove/<int:itemid>', views.remove_menu_item, name='remove'),
    path('edit/<int:itemid>', views.edit_menu_item, name='edit'),
    path('find/', views.get_query, name='get_query'),
    path('orders-list/', views.orders_list, name='orders_list'),
    path('order/<int:order_id>', views.order_detail, name='order_detail')
]