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

# Adds new product
# With clicking on 'Add Product', first, a new dummy product is created, 
# then with the product ID admin is redirected to edit product screen to 
# edit the new product and save the updated information 
# So basically 'adding product' merges with 'updating product' functionality
# Merging Creating and updating product into one saves implementation time 
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser]) # logged in user has to be admin
def createProduct(request): 
    user = request.user 
    product = Product.objects.create(
        user = user,
        name = 'sample name',
        price = 0,
        brand = 'sample brand',
        countInStock = 0,
        category = 'sample category', 
        description = '', 
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

# detail information for single product  
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def updateProduct(request, pk): 
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description'] 

    try:
        product.save()
    except:
        return Response({'message':'Error while adding product'})

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

# delete product   
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser]) # logged in user has to be admin
def deleteProduct(request, pk): 
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response({'message':'product was deleted successfully'}) 
