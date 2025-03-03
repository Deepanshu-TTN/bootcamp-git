from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('order/', views.order_page, name='order_page'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('create-order/', views.create_order, name='create_order'),
    path('order-history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]