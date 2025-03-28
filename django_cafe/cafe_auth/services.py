from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


def create_user(user_data):
    return User.objects.create_user(
        username=user_data["username"],
        password=user_data.get("password") or user_data.get('password1'),
        is_staff=user_data.get('is_staff', False)
    )
    

def get_authenticated_user(form):
    user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'])
    if user is None:
        form.add_error(None, "Invalid Credentials.")
        raise ValidationError("Invalid Credentials.")
    return user