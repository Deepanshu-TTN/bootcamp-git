from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('order/', views.order_page, name='order_page'),
    path('order-place/', views.place_order, name="place_order"),
    path('order-history/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail_customer'),
    path('order-confirm/', views.confirm_order, name='order_confirmation'),
    path('orders/', views.view_orders, name='orders_list_customer')
]