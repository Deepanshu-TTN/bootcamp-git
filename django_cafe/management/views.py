from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView, TemplateView
from django.db.models import Sum, Avg
from django.db.models import Q
from customer.models import Order, OrderItem
from .models import MenuItem
from .forms import MenuItemForm
import json

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

        top_items = OrderItem.objects.values(
            'menu_item__id', 
            'menu_item__name'
        ).annotate(
            count=Sum('item_qty'),
            revenue=Sum('item_total_price')
        ).order_by('-revenue')[:10]
        
        context['top_items'] = top_items
        
        # completed_orders = all_orders.exclude(completed_time=None)
        # if completed_orders.exists():
        #     time_diff_expr = ExpressionWrapper(
        #         F('completed_time') - F('place_time'),
        #         output_field=fields.DurationField()
        #     )
        #     avg_timedelta = completed_orders.annotate(
        #         time_diff=time_diff_expr
        #     ).aggregate(avg_time=Avg('time_diff'))['avg_time']
            
        #     if avg_timedelta:
        #         total_seconds = avg_timedelta.total_seconds()
        #         hours = int(total_seconds // 3600)
        #         minutes = int((total_seconds % 3600) // 60)
        #         seconds = int(total_seconds % 60)
                
        #         if hours > 0:
        #             context['avg_completion_time'] = f"{hours}h {minutes}m"
        #         else:
        #             context['avg_completion_time'] = f"{minutes}m {seconds}s"
        #     else:
        #         context['avg_completion_time'] = "N/A"
        # else:
        #     context['avg_completion_time'] = "N/A"
        
        return context



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