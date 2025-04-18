'''Views for the Auth app'''

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from cafe_auth.forms import SignUpForm, LoginForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from cafe_auth.services import create_user, get_authenticated_user


class SignUp(FormView):
    '''Signup Form View.'''
    form_class = SignUpForm
    template_name = 'signupuser.html'

    def get_success_url(self):
        '''Method override to compute where to redirect the user based on their staff status'''
        if self.request.user.is_staff:
            return reverse_lazy('manage')
        return reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        '''Method override, if user is already authenticated, throw them back to their success page\n
        only show this view when no user is logged in'''
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        '''Method override for custom service integration and login behaviour on success'''
        try:
            self.user = create_user(form.cleaned_data)
            login(self.request, self.user)
            return super().form_valid(form)
        except ValidationError:
            return self.form_invalid(form)
        

class Login(FormView):
    '''Login FormView'''
    form_class = LoginForm
    template_name = 'loginuser.html'

    def get_success_url(self):
        '''Method override to compute where to redirect the user based on their staff status'''
        if self.request.user.is_staff:
            return reverse_lazy('manage')
        return reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        '''Method override, if user is already authenticated, throw them back to their success page\n
        only show this view when no user is logged in'''
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        '''Method override for custom service integration and login behaviour on success'''        
        try:
            user = get_authenticated_user(form)
            # user = form.save()
            # if not user:
            #     return self.form_invalid(form)
            login(self.request, user)
            return super().form_valid(form)
        except ValidationError:
            return self.form_invalid(form)
    

@login_required
def logoutuser(request):
    '''Logout view'''
    logout(request)
    return redirect('home')

    
'''
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
'''




'''
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
            return redirect('home')'''

