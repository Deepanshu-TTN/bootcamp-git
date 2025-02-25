from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

User = get_user_model()

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], 
                                                password=request.POST['password1'], 
                                                is_staff=(request.POST.get('is_staff', False))=='on')
                user.save()
                login(request, user)
                if user.is_staff:
                    return redirect('manage')
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'That username has already been taken. Please choose another username'})
        else:
            return render(request, 'signupuser.html', {'form': UserCreationForm(),
                                                            'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form': AuthenticationForm(),
                                                           'error': 'Username and password did not match'})
        else:
            login(request, user)
            if user.is_staff:
                return redirect('manage')
            return redirect('home')


@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')
