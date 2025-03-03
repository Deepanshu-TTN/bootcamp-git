from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from management.models import MenuItem

User = get_user_model()

order_status_bank = [
    ('pending', 'Pending'),
    ('completed', 'Completed')
]

class Order(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    order_total_price = models.IntegerField()
    order_status = models.CharField(max_length=10, choices=order_status_bank, default='Pending')
    order_place_time = models.DateTimeField(auto_now=True, editable=False)
    order_completed_time = models.DateTimeField(null=True, blank=True)


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