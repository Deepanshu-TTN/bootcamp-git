from django.shortcuts import get_object_or_404
from customer.models import OrderItem, Order

    
def get_user_order_with_items(order_id: int, customer):
    order = get_object_or_404(Order, id=order_id, customer=customer)
    order_items = OrderItem.objects.filter(order_instance=order)
    return order, order_items
    
    
def get_user_orders(user, status):
    # previously had to write all of this
    # orders = Order.objects.filter(customer=user).order_by('-place_time').prefetch_related('orderitem_set')
    return Order.with_items.get_orders_of(user).filter(status__exact=status)
    

def all_orders(status=None):
    qs = Order.with_items.all()
    if status:
        qs.filter(status=status)