from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from customer.models import Order, OrderItem
from .models import MenuItem
from .forms import MenuItemForm


def decorator_is_staff(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        return render(request, 'management/forbidden.html', status=HttpResponseForbidden().status_code)
    return wrapper


@login_required(login_url='/auth/login')
@decorator_is_staff
def manage(request):
    menu_items = MenuItem.objects.all()
    user = request.user
    return render(request, 'management/items_list.html', {'items': menu_items, 'user': user})


@login_required(login_url='/auth/login')
@decorator_is_staff
def create_menu_item(request):
    if request.method == 'GET':
        return render(request, 'management/additem.html', {'form':MenuItemForm()})
    else:
        try:
            menu_item = MenuItemForm(request.POST, request.FILES)
            menu_item.save()
            return redirect('manage')
        except ValueError:
            return render(request, 'management/additem.html', {'form':MenuItemForm(), 'error':'Bad data passed in. Try again.'})


@login_required(login_url='/auth/login')
@decorator_is_staff
def remove_menu_item(request, itemid):
    menu_item = get_object_or_404(MenuItem, pk=itemid)
    if request.method == "POST":
        menu_item.item_image.delete()
        menu_item.delete()
    return redirect('manage')


@login_required(login_url='/auth/login')
@decorator_is_staff
def edit_menu_item(request, itemid):
    menu_item = get_object_or_404(MenuItem, id=itemid)
    if request.method == "GET":            
        item_form = MenuItemForm(instance=menu_item)
        return render(request, 'management/edititem.html', {'form': item_form})
    else:
        try:
            item_form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
            item_form.save()
            return redirect('manage')
        except ValueError:
            return render(request, 'edititem.html', {'form': item_form, 'error': 'Bad data, try again'})


@login_required(login_url='/auth/login')
@decorator_is_staff
def get_query(request):
    search = request.GET.get('search')
    max_price = request.GET.get('lt')

    q=Q()
    if search:
        q &= Q(item_name__contains = search)

    if max_price:
        q &= Q(item_price__lt=max_price)

    menu_items = MenuItem.objects.filter(q)
    return render(request, 'management/items_list.html', {'items':menu_items, 'keyword':search, 'max_price':max_price})


@login_required
@decorator_is_staff
def orders_list(request):
    pending = request.GET.get('p')
    if pending:
        orders = Order.objects.filter(order_status='pending' if pending=='1' else 'completed').order_by('-order_place_time').prefetch_related('orderitem_set')
        return render(request, 'management/orders_list.html', {'orders': orders, 'status':'pending' if pending=='1' else 'completed'})
    orders = Order.objects.order_by('-order_place_time').prefetch_related('orderitem_set')
    return render(request, 'management/orders_list.html', {'orders': orders})
    


@login_required
@decorator_is_staff
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all() 
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        if new_status:
            order.order_status = new_status
            order.save()
            return redirect('order_detail', order_id=order.id)

    return render(request, 'management/order_detail.html', {'order': order, 'order_items': order_items})