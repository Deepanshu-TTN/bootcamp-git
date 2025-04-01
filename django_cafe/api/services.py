'''API services'''
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from management.models import MenuItem
from customer.models import Order, OrderItem
import base64
import logging

def get_image_file(image_data, name):
        '''API service to convert the incoming b64 data into an image file'''
        ## expected format data:image/<image-format>;b64,<binary-data>
        format, imgstr = image_data.split(';b64,') 
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name=f'{name}.{ext}')
        return image_data


def create_order_service(order_data, user):
    order_logger = logging.getLogger('orders')
    
    
    order = Order.objects.create(
        customer=user,
        status='pending'
    )

    log_items = list()
    categories_ordered = set()
    
    for item in order_data['items']:
        ## dont need this as the serializer already checks and shows error message accordingly
        # menu_item = get_object_or_404(MenuItem, pk=item['menu_item']) 
        menu_item = item['menu_item']
        quantity = item['quantity']
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
        f"Order placed - ID: {order.id} | User: {user.username} | "
        f"Time: {order.place_time.strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Categories: {', '.join(categories_ordered)} | "
        f"Total: {order.total_price} | "
        f"Items: {log_items}"
    )
    
    return order
