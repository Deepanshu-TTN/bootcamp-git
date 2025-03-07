from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username',
        help_text="Your username must be unique. We'll let you know if someone has taken it already.",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'aria-describedby': 'usernameHelp'
        })
    )
    
    password1 = forms.CharField(label='Password', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password1'
        })
    )
    
    password2 = forms.CharField(label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password2'
        })
    )
    
    is_staff = forms.BooleanField(required=False, label='Staff Signup?',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'is_staff'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        try:
            validate_password(password1)
        except ValidationError:
            self.add_error('password1', _("Please use a stronger password"))
            raise ValidationError("Please use a stronger password")
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')
            raise ValidationError("Passwords do not match")

        return cleaned_data
    
    def clean_username(self):
        check_username = self.cleaned_data['username'].strip()
        if len(check_username) < 3:
            raise ValidationError("Please use a bigger username.")
        return check_username

    def save(self):
        try:
            user = User.objects.create_user(
                username=self.username, 
                password=self.password1, 
                is_staff=self.is_staff
            )
            return user
        except IntegrityError:
            self.add_error('username', 'That username is already taken :(')
            raise ValidationError('That username is already taken :(')