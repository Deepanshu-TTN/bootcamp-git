'''API-application Views'''

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
from customer.models import Order
from cafe_auth.services import create_user
from management.selectors import get_stats_context
from api.permissions import IsOwnerOrStaffUser, IsStaffUser
from api.services import create_order_service
# from customer.services import update_order_status


## Function based drf view

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user_api(request):
    '''Function based api view for creating a user'''
    if request.data.get('is_staff', False):
        if not request.user.is_authenticated:
            return Response({'error': "Must be logged in to create staff accounts"}, status.HTTP_401_UNAUTHORIZED)
        
        if not request.user.is_superuser:
            return Response({'error': "Only Super User can create staff accounts"}, status.HTTP_403_FORBIDDEN)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        create_user(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
## user views using APIView concrete classes
class UserDetail(generics.RetrieveAPIView):
    '''User Detail API view to retrieve a single object json'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrStaffUser]
    
    def get_object(self):
        '''Overriden get_object method for getting custom user detail if pk provided is "me"'''
        pk = self.kwargs.get('pk')
        if pk == 'me':
            return self.request.user
        return super().get_object()
    
    
class UserList(generics.ListAPIView):
    '''User List API View'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffUser]
    
    
## view using model view set
class MenuItemViewset(viewsets.ModelViewSet):
    '''Model View set for MenuItem Model, provides actions:\n
    post get(list) url: /menu-item/\n
    get(retrieve/detail) put patch delete url:/menu-item/<pk>'''

    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    
    def get_permissions(self):
        '''Method override for custom permission assignments'''
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsStaffUser]
        
        return [permission() for permission in permission_classes]
    
    
    def get_queryset(self):
        '''Method override for applying search param filters'''
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

        return super().get_queryset().filtered_items(search, max_price, category) # custom manager function
    
    
class OrderAPIView(views.APIView):
    '''Custom Order Model DRF APIView with get put post and delete methods'''
    def get_permissions(self):
        '''Method override to show orders based on logged in user only.'''
        if self.request.method in ['PUT', 'DELETE']:
            permission_classes = [IsStaffUser]
        elif self.request.method == "GET":
            permission_classes = [IsOwnerOrStaffUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get(self, request, pk=None):
        '''Get method, if pk provided show specific order after checkin permissions\n
        Show all orders for the user otherwise'''
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
        '''Post method, for order creation'''
        serializer = OrderCreateSerializer(data=request.data, context={'request':request})
        
        if serializer.is_valid():
            # using the serializer create method
            # order = serializer.save()
            
            # using a custom service
            order = create_order_service(serializer.validated_data, request.user)
            
            return Response(OrderSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        '''Put method, for updating status'''
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            # or
            # update_order_status(order, serializer.validated_data.get('status'))
            return Response(OrderSerializer(order, context={'request':request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        '''Delete method, for deleting an order'''
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatisticsAPIView(views.APIView):
    '''Stats API View, returns stats for the application for a staff user'''
    permission_classes = [IsStaffUser]
    
    def get(self, request):
        '''Get method, gets the stats JSON object'''
        
        stats = get_stats_context()
        
        top_items = stats.pop('top_items')        
        for item in top_items:
            item['url'] = request.build_absolute_uri(reverse('menuitem-detail', args={item['item_id']}))
            
        top_categories = top_items = stats.pop('top_categories')
        
        for category in top_categories:
            category['url'] = request.build_absolute_uri(
                reverse('menuitem-list')
                +f"?category={category['category_id']}"
            )
        
        data = {
            'total_revenue': stats.pop('total_revenue', 0),
            'total_orders': stats.pop('total_orders', 0),
            'average_order_value': stats.pop('average_order_value', 0),
            'top_items': top_items,
            'top_categories': top_categories
        }
        
        serializer = StatisticsSerializer(data)
        return Response(serializer.data)
