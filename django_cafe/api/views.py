from rest_framework import status, permissions, views, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Avg, F
from api.serializers import (UserSerializer, MenuItemSerializer, StatisticsSerializer,
    OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer)
from management.models import MenuItem
from customer.models import Order, OrderItem


## Function based drf view

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    if request.data.get('is_staff', False):
        if not request.user.is_authenticated:
            return Response({'error': "Must be logged in to create staff accounts"}, status.HTTP_401_UNAUTHORIZED)
        
        if not request.user.is_superuser:
            return Response({'error': "Only Super User can create staff accounts"}, status.HTTP_403_FORBIDDEN)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


## PERMISSION CLASSES
class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
    

class IsOwnerOrStaffUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff: return True
        
        if hasattr(obj, 'customer'):
            return obj.customer == request.user
        
        return False
    
## user views using APIView concrete classes
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrStaffUser]
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'me':
            return self.request.user
        return super().get_object()
    
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffUser]
    
    
## view using model view set
class MenuItemViewset(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsStaffUser]
        
        return [permission() for permission in permission_classes]
    
    
    def get_queryset(self):
        query = Q()
        
        search = self.request.query_params.get('search', None)
        category = self.request.query_params.get('category', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if search:
            query &= Q(name__icontains=search)
        
        if max_price:
            query &= Q(price__lt=max_price)
        
        if category:
            query &= Q(category=category)

        return super().get_queryset().filter(query)
    
    
class OrderAPIView(views.APIView):
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            permission_classes = [IsStaffUser]
        elif self.request.method == "GET":
            permission_classes = [IsOwnerOrStaffUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get(self, request, pk=None):
        if pk:
            order = get_object_or_404(Order, pk=pk)
            self.check_object_permissions(request=request, obj=order)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        
        if request.user.is_staff:
            orders = Order.with_items.all()
        else:
            orders = Order.with_items.get_orders_of(request.user)

        status_value = request.query_params.get('status')
        if status_value:
            orders = orders.filter(status=status_value)
        
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(data = serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(OrderSerializer(order, context={'request':request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatisticsAPIView(views.APIView):
    permission_classes = [IsStaffUser]
    
    def get(self, request):
        all_orders = Order.objects.all()
        total_orders = all_orders.count()
        total_revenue = all_orders.aggregate(total=Sum('total_price'))['total'] or 0
        average_order_value = all_orders.aggregate(avg=Avg('total_price'))['avg'] or 0
        
        top_items = OrderItem.objects.values(
            item_id=F('menu_item__id'), 
            item_name=F('menu_item__name')
        ).annotate(
            units_sold=Sum('item_qty'),
            revenue=Sum('item_total_price')
        ).order_by('-revenue')[:10]
        
        for item in top_items:
            item['url'] = request.build_absolute_uri(reverse('menuitem-detail', args={item['item_id']}))
            
        top_categories = OrderItem.objects.values(
            category_id=F('menu_item__category'),
        ).annotate(
            category=MenuItem._category_case_statement,
            revenue=Sum('item_total_price'),
        ).order_by('-revenue')[:10]
        
        for category in top_categories:
            category['url'] = request.build_absolute_uri(
                reverse('menuitem-list')
                +f"?category={category['category_id']}"
            )
        
        data = {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'average_order_value': average_order_value,
            'top_items': top_items,
            'top_categories': top_categories
        }
        
        serializer = StatisticsSerializer(data)
        return Response(serializer.data)
