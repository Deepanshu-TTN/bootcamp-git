from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save




class MenuItem(models.Model):
    _catagories = [
        (0, 'Coffee'),
        (1, 'Tea'),
        (2, 'Cookies'),
        (3, 'Muffins'),
        (4, 'Cakes & Cupcakes'),
        (5, 'Pastries'),
        (6, 'Light Bites'),
    ]
    _default_image = 'images/png.webp'

    name = models.CharField(max_length=100, default='')
    price = models.IntegerField(default=0, validators=(
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