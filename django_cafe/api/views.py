from rest_framework import status, permissions, views, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from api.serializers import UserSerializer, MenuItemSerializer
from management.models import MenuItem


## Function based drf view

@api_view(['POST'])
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
