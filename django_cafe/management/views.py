import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView, TemplateView
from django.db.models import Sum, Avg, Q, F
from django.http import Http404
from customer.models import Order, OrderItem
from .models import MenuItem
from .forms import MenuItemForm

'''
def decorator_is_staff(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        return render(request, 'management/forbidden.html', status=HttpResponseForbidden().status_code)
    return wrapper'''


class CheckStaffMixin(LoginRequiredMixin):
    login_url='/auth/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        return render(request, 'management/forbidden.html', status=HttpResponseForbidden().status_code)


class CreateMenuItem(CheckStaffMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'management/additem.html'
    success_url = reverse_lazy('manage')
    

class ManageListView(CheckStaffMixin, ListView):
    model = MenuItem
    paginate_by = 4
    ordering = '-last_update'
    template_name = 'management/manage.html'
    
    def get_queryset(self):
        search = self.request.GET.get('search')
        max_price = self.request.GET.get('lt')
        category = self.request.GET.get('category')

        q=Q()
        if search:
            q &= Q(name__icontains = search)

        if max_price:
            q &= Q(price__lt=max_price)

        if category:
            q &= Q(category=category)
        
        qs = super().get_queryset()
        return qs.filter(q)


class EditMenuItem(CheckStaffMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    pk_url_kwarg = 'itemid'
    template_name = 'management/edititem.html'
    success_url = reverse_lazy('manage')


class DeleteMenuItem(CheckStaffMixin, PermissionRequiredMixin, DeleteView):
    model = MenuItem
    pk_url_kwarg = 'itemid'
    success_url = reverse_lazy('manage')
    permission_required = 'can_delete_menuitems'
    

    
class ManageOrdersListView(CheckStaffMixin, ListView):
    model = Order
    template_name = 'management/orders_list.html'
    
    def get_queryset(self):
        qs = Order.with_items.all()
        status_value = self.request.GET.get('status')
        if status_value:
            qs.filter(status=status_value)
        return qs
    

class ViewOrderDetail(CheckStaffMixin, DetailView):
    model = Order
    template_name = 'management/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.orderitem_set.all()
        context['options'] = Order.status.field.choices
        return context
    

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.POST.get('order_status')

        if new_status:
            order.status = new_status
            order.save()

        return redirect(reverse('order_detail', args=(order.id,)))
    

class OrderStatisticsView(CheckStaffMixin, TemplateView):
    template_name = 'management/order_statistics.html'    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_orders = Order.objects.all()
        context['total_orders'] = all_orders.count()
        context['total_revenue'] = all_orders.aggregate(total=Sum('total_price'))['total'] or 0
        context['average_order_value'] = all_orders.aggregate(avg=Avg('total_price'))['avg'] or 0

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


def upload_order_data(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        
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
                        'id': order_id,
                        'status': 'completed'
                    })

                order_item, _ = OrderItem.objects.get_or_create(
                    menu_item=item,
                    order_instance=order,
                )

                order_item.item_qty += quantity
                order_item.item_total_price = order_item.item_qty * item.price
                order.total_price += order_item.item_total_price
                order_item.save()
                order.save()

            except Http404:
                print(f'could not add data for {row}, model with id: {row[1]} didnt exist.')
                pass

        
        return redirect('orders_list')
    
    return render(request, 'management/offline_data.html')

        




'''
@login_required(login_url='/auth/login')
@decorator_is_staff
def manage(request):
    menu_items = MenuItem.objects.all()
    user = request.user
    return render(request, 'management/manage.html', {'items': menu_items, 'user': user})
'''

'''
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
            messages.error(request, 'Bad data passed in. Try again.')
            return render(request, 'management/additem.html', {'form':MenuItemForm()})
'''

'''
@login_required(login_url='/auth/login')
@decorator_is_staff
def remove_menu_item(request, itemid):
    menu_item = get_object_or_404(MenuItem, pk=itemid)
    if request.method == "POST":
        menu_item.item_image.delete()
        menu_item.delete()
    return redirect('manage')
'''

'''
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
            messages.error(request, 'Bad data passed in. Try again.')
            return render(request, 'edititem.html', {'form': item_form})
'''

'''
@login_required(login_url='/auth/login')
@decorator_is_staff
def get_query(request):
    search = request.GET.get('search')
    max_price = request.GET.get('lt')

    q=Q()
    if search:
        q &= Q(name__contains = search)

    if max_price:
        q &= Q(price__lt=max_price)

    menu_items = MenuItem.objects.filter(q)
    return render(request, 'management/manage.html', {'menuitem_list':menu_items, 'keyword':search, 'max_price':max_price})
'''

'''
@login_required(login_url='/auth/login')
@decorator_is_staff
def orders_list(request):
    status_value = request.GET.get('status')
    if status_value:
        orders = Order.objects.filter(status=status_value).order_by('-place_time').prefetch_related('orderitem_set')
        return render(request, 'management/orders_list.html', {'orders': orders, 'status':status_value})
    orders = Order.objects.order_by('-place_time').prefetch_related('orderitem_set')
   return render(request, 'management/orders_list.html', {'orders': orders})
'''   

'''
@login_required(login_url='/auth/login')
@decorator_is_staff
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all() 
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        if new_status:
            order.status = new_status        
            order.save()
            return redirect('order_detail', order_id=order.id)

    return render(request, 'management/order_detail.html', {'order': order, 'order_items': order_items, 'options': Order.status.field.choices})
'''