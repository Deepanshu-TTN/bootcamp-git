from django.forms import ModelForm
from .models import MenuItem
from django import forms


class MenuItemForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description', 'rating', 'image', 'category']