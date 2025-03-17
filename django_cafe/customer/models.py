from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from management.models import MenuItem
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

order_status_bank = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('canceled', 'Canceled')
]

class OrderOrderItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-place_time').prefetch_related('orderitem_set')
    
    def get_orders_of(self, user):
        return super().get_queryset().filter(customer=user).order_by('-place_time').prefetch_related('orderitem_set')


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, null=True)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    status = models.CharField(max_length=10, choices=order_status_bank, default='pending')
    place_time = models.DateTimeField(auto_now_add=True, editable=False)
    completed_time = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    with_items = OrderOrderItemManager()

    def __str__(self):
        return f"{self.customer.username if self.customer else 'Offline Order'}'s order at {self.place_time}"
    
    def update_total_price(self, save=True):
        total_price = sum(item.item_total_price for item in self.orderitem_set.all())
        self.total_price = total_price
        if save:
            self.save()


@receiver(pre_save, sender=Order)
def check_status(sender, instance, *args, **kwargs):
    if instance.status in ('completed', 'canceled'):
        instance.completed_time = timezone.now()
    
    else:
        instance.completed_time = None
    
    if not instance.pk:
        return


class OrderItem(models.Model):
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
        self.item_total_price = Decimal(self.item_qty) * self.menu_item.price
        if save:
            self.save()
        


@receiver(pre_save, sender=OrderItem)
def update_order_item_price(sender, instance, *args, **kwargs):
    instance.update_item_total_price(False)
    

@receiver(post_save, sender=OrderItem)
def update_order_price(sender, instance, *args, **kwargs):
    if instance.order_instance:
        instance.order_instance.update_total_price()


@receiver(post_delete, sender=OrderItem)
def remove_order_item_from_order(sender, instance, **kwargs):
    if instance.order_instance:
        instance.order_instance.update_total_price()