from django.shortcuts import get_object_or_404
from customer.models import OrderItem, Order

    
def get_user_order_with_items(order_id: int, customer):
    '''Order selector to fetch order and items for given customer\n
    Parameters -> order_id, customer\n
    Returns -> order object, order_items queryset'''
    order = get_object_or_404(Order, id=order_id, customer=customer)
    order_items = OrderItem.objects.filter(order_instance=order)
    return order, order_items
    
    
def get_user_orders(user, status):
    '''Order selector to fetch orders with itemsfor given customer\n
    Parameters -> status, customer\n
    Returns -> order object with prefetched order items'''
    # previously had to write all of this
    # orders = Order.objects.filter(customer=user).order_by('-place_time').prefetch_related('orderitem_set')
    qs = Order.with_items.get_orders_of(user)
    if status:
        return qs.filter(status__exact=status)
    return qs
    

def all_orders(status=None):
    '''Order selector to fetch all orders with given status\n
    \t ONLY USED FOR MANAGEMENT, DONT USE FOR CUSTOMERS'''
    qs = Order.with_items.all()
    if status:
        return qs.filter(status=status)
    return qs