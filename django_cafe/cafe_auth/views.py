from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()

def signupuser(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('manage')
        return redirect('home')
    
    if request.method == 'GET':
        return render(request, 'signupuser.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                validate_password(request.POST['password1'])

                username = request.POST['username']
                password=request.POST['password1']
                staff = (request.POST.get('is_staff', False))=='on'

                user = User.objects.create_user(username=username, password=password, is_staff=staff)
                user.save()
                login(request, user)
                if user.is_staff:
                    return redirect('manage')
                return redirect('home')
            
            except ValidationError:
                return render(request, 'signupuser.html', {'error': 'Invalid Password'})
            except IntegrityError:
                return render(request, 'signupuser.html', {'error': 'That username has already been taken. Please choose another username'})
        else:
            return render(request, 'signupuser.html', {'error': 'Passwords did not match'})


def loginuser(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('manage')
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'loginuser.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', { 'error': 'Username and password did not match'})
        else:
            login(request, user)
            if user.is_staff:
                return redirect('manage')
            return redirect('home')


@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')
