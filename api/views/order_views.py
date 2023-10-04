from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser 

from rest_framework.response import Response  

from api.models import Product, Order, OrderItem, ShippingAddress 
from api.serializers import ProductSerializer, OrderSerializer

from rest_framework import status 
from datetime import datetime 


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def addOrderItems(request): 
    user = request.user 
    data = request.data 

    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0: 
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else: 
        # (1) create order
        order = Order.objects.create(
            user = user ,
            paymentMethod = data['paymentMethod'],
            taxPrice = data['taxPrice'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice'],
            # other fields are created by default, will be changed later 
        ) 
        # (2) create shipping address 
        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country'], 
        )
        # (3) create order items, set order to orderItems relationship  
        for i in orderItems: 
            product = Product.objects.get(_id=i['productId'])
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )
            # (4) update stock 
            product.countInStock -= item.qty 
            product.save() 

        serializer = OrderSerializer(order, many=False)  
        return Response(serializer.data) 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request): 
    user = request.user
    myorders = user.order_set.all()
    serializer = OrderSerializer(myorders, many=True)
    return Response(serializer.data)  


@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def getOrderById(request, pk): 
    user = request.user 
    try: 
        order = Order.objects.get(_id=pk) 
        if user.is_staff or order.user == user: 
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data) 
        else: # user is not authorized 
            Response({'detail':'Not authorized to view this order'}, status=status.HTTP_400_BAD_REQUEST) 
    except: # if order does not exists 
        return Response({'detail':'Not authorized to view this order'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk): 
    order = Order.objects.get(_id=pk) 
    order.isPaid = True
    order.paidAt = datetime.now() 
    order.save() 
    return Response('Order was paid') 
