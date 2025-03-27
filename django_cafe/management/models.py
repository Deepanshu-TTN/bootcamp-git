from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models import Case, When, Value, Q


class MenuItemQueryset(models.QuerySet):
    def filtered_items(self, search=None, max_price=None, category=None):
        q=Q()
        if search:
            q &= Q(name__icontains = search)

        if max_price:
            q &= Q(price__lt=max_price)

        if category:
            q &= Q(category=category)
        
        return self.filter(q)


class MenuItemManager(models.Manager):
    def get_queryset(self):
        return MenuItemQueryset(self.model, using=self.db)
    
    def filtered_items(self, search=None, max_price=None, category=None):
        return self.get_queryset().filtered_items(search, max_price, category)


class MenuItem(models.Model):
    
    class Meta:
        permissions = [
            ("can_delete_menuitems", "Can Delete Menu Items"),
        ]

    _catagories = [
        (0, 'Coffee'),
        (1, 'Tea'),
        (2, 'Cookies'),
        (3, 'Muffins'),
        (4, 'Cakes & Cupcakes'),
        (5, 'Pastries'),
        (6, 'Light Bites'),
    ]
    _category_case_statement = Case(
    When(menu_item__category=0, then=Value('Coffee')),
    When(menu_item__category=1, then=Value('Tea')),
    When(menu_item__category=2, then=Value('Cookies')),
    When(menu_item__category=3, then=Value('Muffins')),
    When(menu_item__category=4, then=Value('Cakes & Cupcakes')),
    When(menu_item__category=5, then=Value('Pastries')),
    When(menu_item__category=6, then=Value('Light Bites')),
    output_field=models.CharField(),
)
    _default_image = 'images/png.webp'

    name = models.CharField(max_length=100, default='')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10, validators=(
        MaxValueValidator(
            limit_value=10000,
            message='Product too expensive!'),
        MinValueValidator(
            limit_value=0,
            message='Please set a higher price'
        )
    ))

    last_update = models.DateTimeField(auto_now=True)
    category = models.IntegerField(default=0, choices=_catagories)
    description = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1,6)], default=5)
    image = models.ImageField(upload_to='images/', null=False, blank=False, default=_default_image)
        
    objects = MenuItemManager()

    def delete(self, using = None, keep_parents = False):
        if self.image.name != self._default_image:
            self.image.delete()
        return super().delete(using, keep_parents)
    
    def __str__(self):
        return self.name


@receiver(pre_save, sender=MenuItem)
def replace_image_from_storage(sender, instance, *args, **kwargs):
    try:
        old_instance = MenuItem.objects.get(id=instance.id)

        if old_instance.image.name != MenuItem._default_image and old_instance.image != instance.image:
            storage = instance.image.storage
            storage.delete(old_instance.image.name)

    except MenuItem.DoesNotExist as e:
        return f'Cannot delete image: {e}'
