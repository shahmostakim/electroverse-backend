from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser 

from rest_framework.response import Response  

from api.models import Product # real data from DB
from api.serializers import ProductSerializer

from rest_framework import status 

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
