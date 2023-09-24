
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from django.contrib.auth.models import User 
from rest_framework.response import Response  

from .products import products # static dummy data  
from .models import Product # real data from DB
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken 

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password 


# this class is responsible for customizing response token  
class MyTokenObtainPairSerializer(TokenObtainPairSerializer): 
    # override the validate method 
    def validate(self, attrs): 
        data = super().validate(attrs) 
        # loop through all fields of user model serializer and prepare response 
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():  
            data[k] = v 

        return data 

# new view class for token customization, extending 'TokenObtainPairView' class 
# that uses a new serializer class for token customization 
class MyTokenObtainPairView(TokenObtainPairView): 
    serializer_class = MyTokenObtainPairSerializer 


# List of API routes 
@api_view(['GET'])
def getRoutes(request): 
    routes = [
        '/api/products/',
        '/api/products/create/',
        '/api/products/upload/',
        '/api/products/<id>/reviews/',
        '/api/products/top/',
        '/api/products/<id>/',
        '/api/products/delete/<id>/',
        '/api/products/update/<id>/',
    ]
    return Response(routes)   


# user registration from forntend 
@api_view(['POST'])
def registerUser(request):

    data = request.data #coming from frontend user registration form 

    # in the frontend, we ask user to put name, email, and password only
    user = User.objects.create(
        first_name = data['name'],
        username = data['email'], # we will not ask 'username' in user registration form, rather use email by default 
        email = data['email'], 
        password = make_password(data['password']) 
    )

    serializer = UserSerializerWithToken(user, many=False) 
    return Response(serializer.data) 


# profile of current user 
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # any logged in user has permission 
def getUserProfile(request): 
    user = request.user 
    serializer = UserSerializer(user, many=False) 
    return Response(serializer.data) 


# list of all users 
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser]) # logged in user has to be admin 
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data) 


# list of products 
@api_view(['GET'])
def getProducts(request): 
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)  

# detail information for single product 
@api_view(['GET'])
def getProduct(request, pk): 
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


