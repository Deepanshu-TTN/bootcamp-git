from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import MenuItem
from .forms import MenuItemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def manage(request):
    menu_items = MenuItem.objects.all()
    user = request.user
    return render(request, 'items_list.html', {'items': menu_items, 'user': user})

@login_required
def create_menu_item(request):
    if request.method == 'GET':
        return render(request, 'additem.html', {'form':MenuItemForm()})
    else:
        try:
            menu_item = MenuItemForm(request.POST, request.FILES)
            menu_item.save()
            return redirect('manage')
        except ValueError:
            return render(request, 'additem.html', {'form':MenuItemForm(), 'error':'Bad data passed in. Try again.'})


@login_required
def remove_menu_item(request, itemid):
    menu_item = get_object_or_404(MenuItem, pk=itemid)
    if request.method == "POST":
        menu_item.delete()
    return redirect('manage')


def edit_menu_item(request, itemid):
    menu_item = get_object_or_404(MenuItem, id=itemid)
    if request.method == "GET":            
        item_form = MenuItemForm(instance=menu_item)
        return render(request, 'edititem.html', {'form': item_form})
    else:
        try:
            item_form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
            item_form.save()
            return redirect('manage')
        except ValueError:
            return render(request, 'edititem.html', {'form': item_form, 'error': 'Bad data, try again'})

def get_query(request):
    search = request.GET.get('search')
    max_price = request.GET.get('lt')

    q=Q()
    if search:
        q &= Q(item_name__contains = search)

    if max_price:
        q &= Q(item_price__lt=max_price)

    menu_items = MenuItem.objects.filter(q)
    return render(request, 'items_list.html', {'items':menu_items, 'keyword':search, 'max_price':max_price})