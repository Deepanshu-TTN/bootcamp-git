from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from customer.models import Order, OrderItem
from management.models import MenuItem
import base64
from django.core.files.base import ContentFile


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=16, min_length=5, required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            UnicodeUsernameValidator
    ])
    password = serializers.CharField(validators=[validate_password], write_only=True)
    is_staff = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            is_staff=validated_data.get('is_staff', False)
        )
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return value


class MenuItemSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'rating', 'category', 
                  'category_display', 'image', 'last_update']
        read_only_fields = ['last_update']
        
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    def _get_image_file(self, image_data, name):
        ## expected format data:image/<image-format>;b64,<binary-data>
        format, imgstr = image_data.split(';b64,') 
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name=f'{name}.{ext}')
        return image_data
    
    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        item_name = validated_data.get('name')
        if image_data:
            validated_data['image'] = self._get_image_file(image_data, item_name)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        image_data = validated_data.pop('image', None)
        item_name = validated_data.get('name', instance.name)
        if image_data:
            validated_data['image'] = self._get_image_file(image_data, item_name)
        return super().update(instance, validated_data)
    

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'item_qty', 'item_total_price']
        read_only_fields = ['item_total_price']
    
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    

class OrderItemCreateSerializer(serializers.Serializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=10)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer = serializers.HyperlinkedRelatedField(
        view_name='users-detail',
        read_only=True
    )
    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_username', 'total_price',
                  'status_display', 'place_time', 'completed_time', 'items']
        read_only_fields = ['total_price', 'place_time', 'completed_time', 'customer']

    
    customer_username = serializers.CharField(source = 'customer.username', read_only=True)
    status_display = serializers.CharField(source = 'get_status_display', read_only=True)
    items = OrderItemSerializer(source='orderitem_set', read_only=True, many=True)


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)
    class Meta:
        model = Order
        fields = ['id', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer = self.context['request'].user
        
        order = Order.objects.create(customer=customer, status='pending')
        
        for item_data in items_data:
            OrderItem.objects.create(
                order_instance=order,
                menu_item=item_data['menu_item'],
                item_qty=item_data['quantity']
            )        
        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        
        
class StatisticsSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_orders = serializers.IntegerField()
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    top_items = serializers.ListField(child=serializers.DictField())
    top_categories = serializers.ListField(child=serializers.DictField())
