from rest_framework import serializers
from django.contrib.auth.models import User 
from rest_framework_simplejwt.tokens import RefreshToken  
from .models import Product, Order, OrderItem, ShippingAddress


class ProductSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Product 
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer): 
    # serializing custom fields 
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = User 
        # these custom fields are returned in access token response 
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']  

    # getter method for custom field '_id', basically returning the default 'id' field
    # this makes user 'id' field consistent with other models in models.py file 
    def get__id(self, obj):  
        return obj.id
    
    # reusing user model's default is_staff field and defining it as 'isAdmin'
    def get_isAdmin(self, obj):  
        return obj.is_staff
    
    # getter method for custom field 'name'
    # basically reusing user.firstname 
    def get_name(self, obj): 
        name = obj.first_name
        if name == '': 
            name = obj.email

        return name 


# extends current User Serializer and includes a token field 
class UserSerializerWithToken(UserSerializer):  
    token = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = User 
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token'] 
    
    def get_token(self, obj): 
        token = RefreshToken.for_user(obj) 
        return str(token.access_token) 


class ShippingAddressSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = ShippingAddress 
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = OrderItem 
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer): 
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = Order 
        fields = '__all__'

    def get_orderItems(self, obj): 
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True) 
        return serializer.data 
    

    def get_shippingAddress(self, obj): 
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data 
        except Exception as e: 
            address = False 
            print("Error: ", e) 
        return address  
    

    def get_user(self, obj): 
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data 

