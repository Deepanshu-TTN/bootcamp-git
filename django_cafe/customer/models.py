from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from management.models import MenuItem
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime

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
    customer = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    total_price = models.IntegerField()
    status = models.CharField(max_length=10, choices=order_status_bank, default='pending')
    place_time = models.DateTimeField(auto_now_add=True, editable=False)
    completed_time = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    with_items = OrderOrderItemManager()

    def __str__(self):
        return f"{self.customer.username}'s order at {self.place_time}"


@receiver(pre_save, sender=Order)
def check_status(sender, instance, *args, **kwargs):
    if instance.status in ('completed', 'canceled'):
        instance.completed_time = datetime.now()
    
    else:
        instance.completed_time = None


class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING, db_constraint=False)
    item_qty = models.IntegerField(validators=[
        MaxValueValidator(
            limit_value=10,
            message='Cannot place more than 10 of the same items!'),
        MinValueValidator(
            limit_value=0,
            message='Invalid quantity provided'
        )
    ])
    order_instance = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_total_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)