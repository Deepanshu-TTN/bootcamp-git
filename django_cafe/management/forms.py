from .models import MenuItem
from django import forms
from management.validators import validate_file_extension


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description', 'rating', 'category']

    image=forms.ImageField(required=False, allow_empty_file=True, validators=[validate_file_extension,])

