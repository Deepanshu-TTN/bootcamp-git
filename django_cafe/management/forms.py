from .models import MenuItem
from django import forms


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'description', 'rating', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'aria-describedby': 'nameHelp',
                'placeholder': 'Enter item name'
                }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'price',
                'placeholder': 'Enter item price'
                }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Enter item description',
                'rows': 3
                }),
            'rating': forms.Select(attrs={
                'class': 'form-control',
                'id': 'rating'
                }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'category'
                }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'image'
                }),
            }