from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class MenuItem(models.Model):
    item_name = models.CharField(max_length=100, default='')
    item_price = models.IntegerField(default=0, validators=(
        MaxValueValidator(
            limit_value=10000,
            message='Product too expensive!'),
        MinValueValidator(
            limit_value=0,
            message='Please set a higher price'
        )
    ))

    item_description = models.TextField()
    item_rating = models.IntegerField(choices=[(i, i) for i in range(1,6)], default=5)
    item_image = models.ImageField(upload_to='images/', null=False, blank=False, default='images/default.png')


    def __str__(self):
        return self.item_name


