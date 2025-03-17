from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from customer.models import Order


class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
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

class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer()

    class Meta:
        model = Order
        fields = '__all__'
