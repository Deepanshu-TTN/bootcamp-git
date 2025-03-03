import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
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
    return render(request, 'customer/order.html', {'menu_items': menu_items})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        menu_item_id = data.get('menu_item_id')
        quantity = data.get('quantity', 1)
        
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        
        cart = request.session.get('cart', {})
        if menu_item_id in cart:
            cart[menu_item_id] = quantity
        else:
            cart[menu_item_id] = quantity
            
        request.session['cart'] = cart
        
        total_price = 0
        cart_items = []
        
        for item_id, qty in cart.items():
            item = MenuItem.objects.get(id=item_id)
            item_total = item.item_price * qty
            total_price += item_total
            cart_items.append({
                'id': item_id,
                'name': item.item_name,
                'price': item.item_price,
                'quantity': qty,
                'total': item_total
            })
        
        return JsonResponse({
            'success': True, 
            'cart_items': cart_items, 
            'total_price': total_price
        })
    
    return JsonResponse({'success': False})

@login_required
def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        menu_item_id = data.get('menu_item_id')
        quantity = data.get('quantity')
        
        if quantity <= 0:
            cart = request.session.get('cart', {})
            if menu_item_id in cart:
                del cart[menu_item_id]
                request.session['cart'] = cart
        else:
            cart = request.session.get('cart', {})
            cart[menu_item_id] = min(quantity, 10) 
            request.session['cart'] = cart
        
        total_price = 0
        cart_items = []
        
        for item_id, qty in cart.items():
            item = MenuItem.objects.get(id=item_id)
            item_total = item.item_price * qty
            total_price += item_total
            cart_items.append({
                'id': item_id,
                'name': item.item_name,
                'price': item.item_price,
                'quantity': qty,
                'total': item_total
            })
        
        return JsonResponse({
            'success': True, 
            'cart_items': cart_items, 
            'total_price': total_price
        })
    
    return JsonResponse({'success': False})

@login_required
def create_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        if not cart:
            return JsonResponse({'success': False, 'message': 'Cart is empty'})
        
        total_price = 0
        for item_id, qty in cart.items():
            item = MenuItem.objects.get(id=item_id)
            total_price += item.item_price * qty
        
        order = Order.objects.create(
            customer_id=request.user,
            order_total_price=total_price,
            order_status='pending'
        )
        
        for item_id, qty in cart.items():
            menu_item = MenuItem.objects.get(id=item_id)
            item_total = menu_item.item_price * qty
            
            OrderItem.objects.create(
                menu_item=menu_item,
                item_qty=qty,
                order_instance=order,
                item_total_price=item_total
            )
        
        request.session['cart'] = {}
        
        return JsonResponse({
            'success': True, 
            'order_id': order.id,
            'message': 'Order placed successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

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
        'order_items': order_items
    })
