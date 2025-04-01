from django.db.models import Sum, Avg, Count
from customer.models import Order, OrderItem
from management.models import MenuItem


def get_items():
    '''Management selector to get all menuitems'''
    return MenuItem.objects.all()


def get_top_items_bycount(limit: int = 4):
    '''Management selector to get top items by count\n
    Parameters -> limit: int(default 4)'''
    top_items_by_count = OrderItem.objects.values(
        'menu_item',
    ).annotate(
        count = Sum('item_qty'),
    ).order_by('-count')[:limit]
    menu_item_ids = [item['menu_item'] for item in top_items_by_count]
    return MenuItem.objects.filter(id__in=menu_item_ids)  


def get_items_query(search='', max_price=None, category=None):
    '''Management selector to get items based on given query'''
    return MenuItem.objects.filtered_items(search, max_price, category)


def get_stats_context(context: dict = dict()) -> dict:
    '''Management selector to add to a context dictionary stats of the website\n
    Parameters -> context: dictionary(can be empty)\n
    Returns -> dictionary with the following stats:\n
    \tTotal Orders, Total Revenue, Average Order Value, Top sold items by revenue, Top selling categories'''
    all_orders = Order.objects.all()
    print(all_orders[4].orderitem_set.all())
    
    # context['total_orders'] = all_orders.count()
    # context['total_revenue'] = all_orders.aggregate(total=Sum('total_price'))['total'] or 0
    # context['average_order_value'] = all_orders.aggregate(avg=Avg('total_price'))['avg'] or 0
    # optimized
    nums = all_orders.aggregate(
        total=Sum('total_price'), 
        avg=Avg('total_price'),
        count=Count('id'))
    context['total_revenue'] = nums.get('total', 0)
    context['total_orders'] = nums.get('count', 0)
    context['average_order_value'] = nums.get('avg', 0)

    # select final.name, sum(item_total_price) as revenue from 
    # (select mgmt.name, cust.item_total_price from management_menuitem as mgmt 
    # join customer_orderitem cust on cust.menu_item_id = mgmt.id)
    # as final group by final.name order by revenue desc limit 10;
    top_items = OrderItem.objects.values(
        'menu_item__id', 
        'menu_item__name'
    ).annotate(
        count = Sum('item_qty'),
        revenue = Sum('item_total_price')
    ).order_by('-revenue')[:10]
    context['top_items'] = top_items   

    # select management_menuitem.category, sum(customer_orderitem.item_total_price) as rev 
    # from management_menuitem join customer_orderitem 
    # on customer_orderitem.menu_item_id = management_menuitem.id 
    # group by management_menuitem.category order by rev desc;
    top_categories = OrderItem.objects.values(
        'menu_item__category',
    ).annotate(
        category = MenuItem._category_case_statement,
        revenue = Sum('item_total_price'),
    ).order_by('-revenue')[:10]
    
    context['top_categories']=top_categories

    return context

