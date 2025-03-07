from .models import MenuItem
from django import forms


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description', 'rating', 'image', 'category']