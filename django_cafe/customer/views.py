from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum, F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from management.models import MenuItem
from .models import Order, OrderItem
import logging

order_logger = logging.getLogger('orders')


def home(request):
    user = request.user if str(request.user)!='AnonymousUser' else None
    top_items_by_count = OrderItem.objects.values(
            'menu_item',
        ).annotate(
            count = Sum('item_qty'),
        ).order_by('-count')[:4]
    menu_item_ids = [item['menu_item'] for item in top_items_by_count]

    top_items = MenuItem.objects.filter(id__in=menu_item_ids)
    
    return render(request, 'customer/home.html', {'items': top_items, 'user': user, 'categories': MenuItem._catagories})



def search(request):
    search = request.GET.get('search')
    max_price = request.GET.get('lt')
    category = request.GET.get('category')

    user = request.user if str(request.user)!='AnonymousUser' else None

    q=Q()
    if search:
        q &= Q(name__icontains = search)

    if max_price:
        q &= Q(price__lt=max_price)

    if category:
        q &= Q(category=category)
        
    menu_items = MenuItem.objects.filter(q)
    return render(request, 'customer/search.html', {'items': menu_items, 'user': user, 'keyword': search, 'max_price':max_price})


@login_required(login_url='/auth/login')
def order_page(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'customer/order.html', {'items': menu_items})

@login_required(login_url='/auth/login')
def place_order(request):
    if request.method == 'POST':
        selected_items = dict()
        for key, value in request.POST.items():
            if key.startswith('quantity_') and int(value) > 0:
                item_id = key.replace('quantity_', '')
                selected_items[item_id] = int(value)
        
        if not selected_items:
            messages.error(request, 'Please select at least one item to order.')
            return redirect('order_page')
        
        order_items = []
        total_price = 0
        
        for item_id, quantity in selected_items.items():
            menu_item = get_object_or_404(MenuItem, id=item_id)
            
            order_items.append({
                'menu_item': item_id,
                'quantity': quantity,
                'item_name': menu_item.name
            })

            total_price+=menu_item.price*quantity
        
        request.session['order_preview'] = [(item['menu_item'], item['quantity']) for item in order_items]
        
        return render(request, 'customer/order_confirmation.html', {
            'items': order_items,
            'total_price': total_price
        })
    
    return redirect('order_page')

@login_required(login_url='/auth/login')
def confirm_order(request):
    if request.method == 'POST':
        order_data = request.session.get('order_preview')
        
        if not order_data:
            messages.error(request, 'Your order session has expired. Please start again.')
            return redirect('order_page')
        
        order = Order.objects.create(
            customer=request.user,
            status='pending'
        )

        log_items = list()
        categories_ordered = set()
        
        for item in order_data:
            menu_item = get_object_or_404(MenuItem, pk=item[0])
            quantity = item[1]
            OrderItem.objects.create(
                menu_item=menu_item,
                item_qty=quantity,
                order_instance=order,
            )

            log_items.append({
                'item_name': menu_item.name,
                'item_id': menu_item.id,
                'category': menu_item.get_category_display(),
                'quantity': quantity,
                'price': menu_item.price,
            })
            categories_ordered.add(menu_item.get_category_display())

        order.update_total_price()

        order_logger.info(
            f"Order placed - ID: {order.id} | User: {request.user.username} | "
            f"Time: {order.place_time.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"Categories: {', '.join(categories_ordered)} | "
            f"Total: {order.total_price} | "
            f"Items: {log_items}"
        )
        
        
        if 'order_preview' in request.session:
            del request.session['order_preview']
        
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_detail_customer', order_id=order.id)
    
    return redirect('order_page')


@login_required(login_url='/auth/login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    order_items = OrderItem.objects.filter(order_instance=order)
    
    return render(request, 'customer/order_detail.html', {
        'order': order,
        'items': order_items
    })


@login_required(login_url='/auth/login')
def view_orders(request):
    user = request.user
    # previously had to write all of this
    # orders = Order.objects.filter(customer=user).order_by('-place_time').prefetch_related('orderitem_set')
    status_value = request.GET.get('status')
    q = Q()
    if status_value:
        q &= Q(status__exact=status_value)
        
    orders = Order.with_items.get_orders_of(user).filter(q)
    return render(request, 'customer/orders_list.html', {'orders': orders})
