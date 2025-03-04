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

class Order(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    order_total_price = models.IntegerField()
    order_status = models.CharField(max_length=10, choices=order_status_bank, default='pending')
    order_place_time = models.DateTimeField(auto_now=True, editable=False)
    order_completed_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer_id.username}'s order at {self.order_place_time}"


@receiver(pre_save, sender=Order)
def check_status(sender, instance, *args, **kwargs):
    if instance.order_status in ('completed', 'canceled'):
        instance.order_completed_time = datetime.now()


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