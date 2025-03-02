from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from management.models import MenuItem


def home(request):
    search = request.GET.get('search')
    max_price = request.GET.get('lt')

    q=Q()
    if search:
        q &= Q(item_name__contains = search)

    if max_price:
        q &= Q(item_price__lt=max_price)
    menu_items = MenuItem.objects.filter(q)
    return render(request, 'customer/items_list.html', {'items': menu_items})

# Create your views here.
