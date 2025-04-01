'''Customer URLs'''

from django.urls import path
from . import views

urlpatterns = [
    # landing page
    path('', views.home, name='home'),
    
    # search page
    path('search/', views.search, name='search'),
    
    # place order
    path('order/', views.order_page, name='order_page'),
    path('order-place/', views.place_order, name="place_order"),
    
    # order operations
    path('orders/<int:order_id>/', views.order_detail, name='order_detail_customer'),
    path('order-confirm/', views.confirm_order, name='order_confirmation'),
    path('orders/', views.view_orders, name='order_history')
]