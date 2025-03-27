from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import BadRequest
from django.http import Http404
from django.contrib.auth.decorators import login_required
from management.models import MenuItem
from management.selectors import get_top_items_bycount, get_items_query, get_items
from customer.services import create_order_preview, confirm_and_create_order
from customer.selectors import get_user_order_with_items, get_user_orders


def home(request):
    user = request.user if str(request.user)!='AnonymousUser' else None
    top_items_by_count = get_top_items_bycount(limit=4)
    return render(request, 'customer/home.html', {
        'items': top_items_by_count, 
        'user': user, 
        'categories': MenuItem._catagories
    })


def search(request):
    user = request.user if str(request.user)!='AnonymousUser' else None
    search = request.GET.get('search')
    max_price = request.GET.get('lt')
    category = request.GET.get('category')
    menu_items = get_items_query(search, max_price, category)
    
    return render(request, 'customer/search.html', {
        'items': menu_items, 
        'user': user, 
        'keyword': search, 
        'max_price':max_price
    })


@login_required(login_url='/auth/login')
def order_page(request):
    return render(request, 'customer/order.html', {'items': get_items()})


@login_required(login_url='/auth/login')
def place_order(request):
    if request.method == 'POST':
        try:
            order_items, total_price = create_order_preview(request)
            return render(request, 'customer/order_confirmation.html', {
                'items': order_items,
                'total_price': total_price
            })

        except BadRequest as e:
            messages.error(request, str(e))
            return redirect('order_page')
        
        except Http404 as e:
            messages.error(request, str(e))
            return redirect('order_page')

    return redirect('order_page')


@login_required(login_url='/auth/login')
def confirm_order(request):
    if request.method == 'POST':
        try:
            new_order = confirm_and_create_order(request)
            return redirect('order_detail_customer', order_id=new_order)
        
        except BadRequest as e:
            messages.error(request, str(e))
            return redirect('order_page')
        
        except Http404 as e:
            messages.error(request, str(e))
            return redirect('order_page')

    return redirect('order_page')


@login_required(login_url='/auth/login')
def order_detail(request, order_id):
    try:
        order, order_items = get_user_order_with_items(order_id, request.user)
        
        return render(request, 'customer/order_detail.html', {
            'order': order,
            'items': order_items
        })
    except Http404 as e:
        messages.error(request, str(e))
        return redirect('order_page')


@login_required(login_url='/auth/login')
def view_orders(request):
    user = request.user
    status_value = request.GET.get('status')
    orders = get_user_orders(user, status_value)
    
    return render(request, 'customer/orders_list.html', {'orders': orders, 'status': status_value})
