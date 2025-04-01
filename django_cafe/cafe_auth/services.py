from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


def create_user(user_data):
    '''User creation service, returns a newly created user or 
    raises DB errors which need to be handled.'''
    return User.objects.create_user(
        username=user_data["username"],
        password=user_data.get("password") or user_data.get('password1'),
        is_staff=user_data.get('is_staff', False)
    )
    

def get_authenticated_user(form):
    '''Return a user based on submitted form, \n
    Parameters -> form (Form class object)\n
    Returns -> user if data is correct\n
    Raises -> on incorrect data Validation error after adding to the form'''
    user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'])
    if user is None:
        form.add_error(None, "Invalid Credentials.")
        raise ValidationError("Invalid Credentials.")
    return user