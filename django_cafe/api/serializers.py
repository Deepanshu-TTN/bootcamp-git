'''Serializers for the django cafe API'''
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from customer.models import Order, OrderItem
from management.models import MenuItem
from api.services import get_image_file


class UserSerializer(serializers.Serializer):
    '''Custom User serializer\n Fields: `id`(readonly), `username`, `password`, `is_staff`'''
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=16, min_length=5, required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            UnicodeUsernameValidator
    ])
    password = serializers.CharField(validators=[validate_password], write_only=True)
    is_staff = serializers.BooleanField(required=False)

    # redid in services.
    # def create(self, validated_data):
    #     return User.objects.create_user(
    #         username=validated_data["username"],
    #         password=validated_data["password"],
    #         is_staff=validated_data.get('is_staff', False)
    #     )
    
    def validate_password(self, value):
        '''Implemented for custom validation other than `validators` field in defination'''
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return value


class MenuItemSerializer(serializers.ModelSerializer):
    '''Menu Item Model Serializer\n Fields: `id` `name`, `price`, `description`\n,
    `rating`, `category`, `category_display`, `image`(input as b64), `last_update`(readonly)'''
    image = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    
    class Meta:
        '''Define metadata for the serializer'''
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'rating', 'category', 
                  'category_display', 'image', 'last_update']
        read_only_fields = ['last_update']
        
    # source parameter already assumes 'MenuItem' attribute, 
    # so we can write MenuItem.get_category_display as:
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    # redid all this in api.services
    # def _get_image_file(self, image_data, name):
    #     '''Serializer method to convert the incoming b64 data into an image file'''
    #     ## expected format data:image/<image-format>;b64,<binary-data>
    #     format, imgstr = image_data.split(';b64,') 
    #     ext = format.split('/')[-1]
    #     image_data = ContentFile(base64.b64decode(imgstr), name=f'{name}.{ext}')
    #     return image_data
    
    def create(self, validated_data):
        '''Overwritten create method to take in image data as b64 and process it before storing'''
        image_data = validated_data.pop('image', None)
        item_name = validated_data.get('name')
        if image_data:
            validated_data['image'] = get_image_file(image_data, item_name)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        '''Overwritten update method to take in image data as b64 and process it before storing'''
        image_data = validated_data.pop('image', None)
        item_name = validated_data.get('name', instance.name)
        if image_data:
            validated_data['image'] = get_image_file(image_data, item_name)
        return super().update(instance, validated_data)
    

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    '''OrderItem Model Serializer\nContains hyperlinks for menu_items,\n
    Fields: `id`, `menu_item`(hyperlink), `item_qty`, `item_total_price`(readonly)'''
    class Meta:
        '''Define metadata for the serializer'''
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'item_qty', 'item_total_price']
        read_only_fields = ['item_total_price']
    
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    

class OrderItemCreateSerializer(serializers.Serializer):
    '''Use for OrderItem Serializer: converting incoming item and quantity values to python\n
    Fields: `menu_item`(id), `quantity`'''
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=10)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    '''Order Model Serializer with hyperlinks for items-menu-items and customers\n
    Fields: `id`, `customer`(readonly hyperlink), `customer_username`, `total_price`(readonly),\n
    `status_display`, `place_time`(readonly), `completed_time`(readonly), `items`'''
    customer = serializers.HyperlinkedRelatedField(
        view_name='users-detail',
        read_only=True
    )
    class Meta:
        '''Define metadata for the serializer'''
        model = Order
        fields = ['id', 'customer', 'customer_username', 'total_price',
                  'status_display', 'place_time', 'completed_time', 'items']
        read_only_fields = ['total_price', 'place_time', 'completed_time', 'customer']

    
    customer_username = serializers.CharField(source = 'customer.username', read_only=True)
    status_display = serializers.CharField(source = 'get_status_display', read_only=True)
    items = OrderItemSerializer(source='orderitem_set', read_only=True, many=True)


class OrderCreateSerializer(serializers.ModelSerializer):
    '''Use for Order Serializer: converting incoming items list to python\n
    Fields: `items`( `menu_item`(id), `quantity`),'''
    items = OrderItemCreateSerializer(many=True, write_only=True)
    class Meta:
        '''Define metadata for the serializer'''
        model = Order
        fields = ['id', 'items']
    
    ## using service but this works too :)
    def create(self, validated_data):
        '''Overwritten the create method for this model serializer for custom behaviour'''
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
    '''Use for Order Serializer: convert incoming status value to python'''
    class Meta:
        model = Order
        fields = ['status']
        
    ## Model serializer already provides this validation
    # def validate_status(self, incoming_status):
    #     if incoming_status not in ['pending', 'completed', 'canceled']:
    #         raise serializers.ValidationError("Invalid status value.")
    #     return incoming_status
        
        
class StatisticsSerializer(serializers.Serializer):
    '''Stats Serializer'''
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_orders = serializers.IntegerField()
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    top_items = serializers.ListField(child=serializers.DictField())
    top_categories = serializers.ListField(child=serializers.DictField())
