from django.urls import path
from . import views

urlpatterns = [
    path('', views.ManageListView.as_view(), name='manage'),
    path('additem/', views.CreateMenuItem.as_view(), name='additem'),
    path('remove/<int:itemid>', views.DeleteMenuItem.as_view(), name='remove'),
    path('edit/<int:itemid>', views.EditMenuItem.as_view(), name='edit'),
    path('orders-list/', views.ManageOrdersListView.as_view(), name='orders_list'),
    path('order/<int:order_id>', views.ViewOrderDetail.as_view(), name='order_detail'),
    path('stats/', views.OrderStatisticsView.as_view(), name='stats')
]