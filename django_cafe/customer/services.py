from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.core.exceptions import BadRequest
from customer.models import Order, OrderItem
from management.models import MenuItem
import openpyxl
import logging


def _get_selected_items(request)->dict:
    '''Helper function to creating order session\n
    Takes in request as parameter and for all the POST items in the request\n
    returns the item id and quantity selected from the POST in form of a dict'''
    selected_items = dict()
    for key, value in request.POST.items():
        if key.startswith('quantity_') and int(value) > 0:
            item_id = key.replace('quantity_', '')
            selected_items[item_id] = int(value)
    return selected_items


def create_order_preview(request) -> tuple[list, float]:
    '''Customer Service to create a request session from selected items\n
    from POST items and returns the items list and total price\n
    Parameters -> request\n
    Returns -> order_items: List, total_price: float'''
    selected_items = _get_selected_items(request)
    if not selected_items:
        raise BadRequest('Please select at least one item to order.')
    
    order_items = []
    total_price = 0.0
    
    for item_id, quantity in selected_items.items():
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        order_items.append({
            'menu_item': item_id,
            'quantity': quantity,
            'item_name': menu_item.name,
            'price': menu_item.price*quantity
        })

        total_price+=float(menu_item.price)*quantity
    
    request.session['order_preview'] = [(item['menu_item'], item['quantity']) for item in order_items]
    return order_items, total_price


def confirm_and_create_order(request):
    '''Customer service to create order from given request\n
    Request should contain : user, order_preview dict in session\n
    Returns newly created order id'''
    order_logger = logging.getLogger('orders')
    order_data = request.session.get('order_preview')
    
    if not order_data:
        raise BadRequest('Your order session has expired. Please start again.')
    
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
    return order.id


def update_order_status(order: Order, status: str):
    '''Customer Service to update status of an order instance.\n
    Parameters -> order: Order Instance, status: New Status'''
    # if form submitted has the same status as current instance do nothing
    if order.status == status:
        return None

    # update order status if the new status is recieved
    order.status = status
    order.save()
    return None


def bulk_order_from_data(excel_file):
    '''Service which adds Order and OrderItem data from an excel file\n
    Parameters -> excel_file: A file\n
    Logs faulty model ids encountered in the terminal'''
    wb = openpyxl.load_workbook(excel_file)
    worksheet = wb.active

    for row in worksheet.iter_rows(values_only=True):
        try:
            item_id = int(row[0])
            item = get_object_or_404(MenuItem, id=item_id)
            quantity = int(row[1])

            #assuming related data is already stored and
            #we need to add items to an old order
            order_id = int(row[2])
            order, _ = Order.objects.get_or_create(
                id=order_id,
                defaults={
                    'status': 'completed'
                })

            order_item, _ = OrderItem.objects.get_or_create(
                menu_item=item,
                order_instance=order,
            )

            order_item.item_qty += quantity
            order_item.save()

        except Http404:
            print(f'could not add data for {row}, model with id: {row[1]} didnt exist.')
            pass
        

