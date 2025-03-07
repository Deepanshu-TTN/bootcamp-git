from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from cafe_auth.forms import SignUpForm

User = get_user_model()

def signupuser(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('manage')
        return redirect('home')
    
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'signupuser.html', {'form': form})
    else:
        try:
            form = SignUpForm(request.POST)
            user = form.save()
            login(request,user)
            if user.is_staff:
                return redirect('manage')
            return redirect('home')            
        except:
            return render(request, 'signupuser.html', {'form':form})


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
