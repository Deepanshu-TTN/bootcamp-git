from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView, TemplateView
from customer.models import Order
from .models import MenuItem
from .forms import MenuItemForm
from management.selectors import get_stats_context, get_items_query
from customer.services import update_order_status, bulk_order_from_data
from customer.selectors import all_orders

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

        return get_items_query(search, max_price, category) 


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
    context_object_name = 'orders' # <modelname>_list otherwise, here order_list
    
    def get_queryset(self):
        status_value = self.request.GET.get('status')
        return all_orders(status_value).select_related('customer')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status')
        return context


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
        update_order_status(order, new_status)
        return redirect(reverse('order_detail', args=(order.id,)))
    

class OrderStatisticsView(CheckStaffMixin, TemplateView):
    template_name = 'management/order_statistics.html'    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_stats_context(context)


def upload_order_data(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        bulk_order_from_data(excel_file)        
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