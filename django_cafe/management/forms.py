from django.forms import ModelForm
from .models import MenuItem


class MenuItemForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = ['item_name', 'item_price', 'item_description', 'item_rating', 'item_image', 'category']