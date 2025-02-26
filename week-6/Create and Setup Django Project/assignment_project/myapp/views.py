from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>MyAPP page!</h1>')


def greet(request):
    dummy_user = 'Deepanshu'
    return render(request, 'greet.html', {'user': dummy_user})