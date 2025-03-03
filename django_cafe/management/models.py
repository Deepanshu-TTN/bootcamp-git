from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

catagories = [
    (0, 'Coffee'),
    (1, 'Tea'),
    (2, 'Cookies'),
    (3, 'Muffins'),
    (4, 'Cakes & Cupcakes'),
    (5, 'Pastries'),
    (6, 'Light Bites'),
]

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
    category = models.IntegerField(default=0, choices=catagories)
    item_description = models.TextField()
    item_rating = models.IntegerField(choices=[(i, i) for i in range(1,6)], default=5)
    item_image = models.ImageField(upload_to='images/', null=False, blank=False, default='images/default.png')



    def __str__(self):
        return self.item_name


