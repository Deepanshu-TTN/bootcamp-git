'''Customer Models'''

from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from management.models import MenuItem


User = get_user_model()

order_status_bank = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('canceled', 'Canceled')
]


class OrderOrderItemManager(models.Manager):
    '''
    Manager for handling orders with related order items.\n
    This manager provides methods for retrieving orders with their associated order items\n
    and ensures that the order items are prefetched for efficiency.
    '''

    def get_queryset(self):
        '''
        Returns the default queryset for orders, ordered by `place_time` in descending order.\n
        Also, it prefetches the related `orderitem_set` for each order to reduce database queries.
        '''
        return super().get_queryset().order_by('-place_time').prefetch_related('orderitem_set__menu_item')

    def get_orders_of(self, user):
        '''
        Retrieves the orders for a specific user, ordered by `place_time` in descending order.
        \nIt also prefetches the related `orderitem_set` for each order to optimize query performance.
        \nParameters -> user (User): The user whose orders are to be retrieved.
        \nReturns -> QuerySet: A queryset of orders placed by the specified user with 
            their related order items prefetched.
        '''
        return self.get_queryset().filter(customer=user).order_by('-place_time').select_related('customer').prefetch_related('orderitem_set__menu_item')
        # for further optimization we can also use .only() and pass in only the field names we want



class Order(models.Model):
    '''Order Model for handling user order objects and communicating with the database'''
    customer = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, null=True)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    status = models.CharField(max_length=10, choices=order_status_bank, default='pending')
    place_time = models.DateTimeField(auto_now_add=True, editable=False)
    completed_time = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    with_items = OrderOrderItemManager()

    def __str__(self):
        return f"{self.customer.username if self.customer
                    else 'Offline Order'}'s order at {self.place_time}"
    
    
    def update_total_price(self, save=True):
        '''Updates the total price of the order based on the prices of the related order items.\n
        Parameters -> save (bool): If True, the order is saved after updating the total price.\n
        (to prevent circular calling )
        '''
        total_price = sum(item.item_total_price for item in self.orderitem_set.all())
        self.total_price = total_price
        if save:
            self.save()


@receiver(pre_save, sender=Order)
def check_status(sender, instance, *args, **kwargs):
    '''Check status reciever, whenever db is going to be updated with a new order instance\n
    if the status is changed, updates the completion time for the order before writing on.\n
    Saves these changes together.'''
    if instance.status in ('completed', 'canceled'):
        instance.completed_time = timezone.now()

    else:
        instance.completed_time = None



class OrderItem(models.Model):
    '''Order item model'''
    menu_item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING, db_constraint=False)
    item_qty = models.IntegerField(default=0, validators=[
        MaxValueValidator(
            limit_value=10,
            message='Cannot place more than 10 of the same items!'),
        MinValueValidator(
            limit_value=0,
            message='Invalid quantity provided'
        )
    ])
    order_instance = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_total_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)


    def update_item_total_price(self, save=True):
        '''Updates the total price of the item based on the quantity and price of the menu item.\n
        Parameters -> save (bool): If True, the item is saved after updating the total price.\n
        (to prevent circular calling )'''
        self.item_total_price = Decimal(self.item_qty) * self.menu_item.price
        if save:
            self.save()
        

@receiver(pre_save, sender=OrderItem)
def update_order_item_price(sender, instance, *args, **kwargs):
    '''Recalculate the order total price when an order item is updated'''
    instance.update_item_total_price(False)
    

@receiver(post_save, sender=OrderItem)
def update_order_price(sender, instance: OrderItem, *args, **kwargs):
    '''Update order price when a new order item is created'''
    if instance.order_instance:
        instance.order_instance.update_total_price()


@receiver(post_delete, sender=OrderItem)
def remove_order_item_from_order(sender, instance: OrderItem, **kwargs):
    '''Update order price when an order item is deleted'''
    if instance.order_instance:
        instance.order_instance.update_total_price()