from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from management.models import MenuItem
from .models import Order, OrderItem


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


@login_required
def order_page(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'customer/order.html', {'items': menu_items})

@login_required
def place_order(request):
    if request.method == 'POST':
        selected_items = {}
        for key, value in request.POST.items():
            if key.startswith('quantity_') and int(value) > 0:
                item_id = key.replace('quantity_', '')
                selected_items[item_id] = int(value)
        
        if not selected_items:
            messages.error(request, 'Please select at least one item to order.')
            return redirect('order_page')
        
        total_price = 0
        order_items = []
        
        for item_id, quantity in selected_items.items():
            menu_item = get_object_or_404(MenuItem, id=item_id)
            item_total = menu_item.item_price * quantity
            total_price += item_total
            
            order_items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'item_total': item_total
            })
        
        request.session['order_preview'] = {
            'items': [(item['menu_item'].id, item['quantity']) for item in order_items],
            'total_price': total_price
        }
        
        return render(request, 'customer/order_confirmation.html', {
            'items': order_items,
            'total_price': total_price
        })
    
    return redirect('order_page')

@login_required
def confirm_order(request):
    if request.method == 'POST':
        order_data = request.session.get('order_preview')
        
        if not order_data:
            messages.error(request, 'Your order session has expired. Please start again.')
            return redirect('order_page')
        print(request.user)
        order = Order.objects.create(
            customer_id=request.user,
            order_total_price=order_data['total_price'],
            order_status='pending'
        )
        
        for item_id, quantity in order_data['items']:
            menu_item = get_object_or_404(MenuItem, id=item_id)
            item_total = menu_item.item_price * quantity
            
            OrderItem.objects.create(
                menu_item=menu_item,
                item_qty=quantity,
                order_instance=order,
                item_total_price=item_total
            )
        
        if 'order_preview' in request.session:
            del request.session['order_preview']
        
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_detail', order_id=order.id)
    
    return redirect('order_page')

@login_required
def order_history(request):
    orders = Order.objects.filter(customer_id=request.user).order_by('-order_place_time')
    return render(request, 'customer/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer_id=request.user)
    order_items = OrderItem.objects.filter(order_instance=order)
    
    return render(request, 'customer/order_detail.html', {
        'order': order,
        'items': order_items
    })
