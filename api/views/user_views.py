from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from django.contrib.auth.models import User 
from rest_framework.response import Response  
 
from api.models import Product # real data from DB
from api.serializers import ProductSerializer, UserSerializer, UserSerializerWithToken 

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password 
from rest_framework import status  


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


# user registration from forntend 
@api_view(['POST'])
def registerUser(request):

    data = request.data #coming from frontend user registration form 

    # in the frontend, we ask user to put name, email, and password only
    try: 
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'], # we will not ask 'username' in user registration form, rather use email by default 
            email = data['email'], 
            password = make_password(data['password']) 
        )

        serializer = UserSerializerWithToken(user, many=False) 
        return Response(serializer.data)
    except: 
        message = {'detail': 'User with this email already exists'}  
        return Response(message, status=status.HTTP_400_BAD_REQUEST) 


# profile of current user 
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # any logged in user has permission 
def getUserProfile(request): 
    user = request.user 
    serializer = UserSerializer(user, many=False) 
    return Response(serializer.data) 


# update profile of current user 
@api_view(['PUT'])
@permission_classes([IsAuthenticated]) # any logged in user has permission 
def updateUserProfile(request): 
    user = request.user 
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data 

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '': 
        user.password = make_password(data['password'])  

    user.save() 

    return Response(serializer.data)


# list of all users except logged in user 
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser]) # logged in user has to be admin 
def getUsers(request): # get list of all users except himself
    logged_in_user = request.user
    # Exclude the logged-in user from the queryset
    users = User.objects.exclude(pk=logged_in_user.pk)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)  


# get user profile (except logged in user) for updating profile info  
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser]) # logged in user has to be admin 
def getUserById(request, pk): # get list of all users except himself
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)  


# update another user profile (except logged in user) 
@api_view(['PUT'])
@permission_classes([IsAuthenticated]) # any logged in user has permission 
def updateUser(request, pk): 
    user = User.objects.get(id=pk) 
    data = request.data 

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    try: 
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except: 
        return Response('Error while updating user. Please check database connection')
     

# Delete user functionality 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser]) # logged in user has to be admin
def deleteUser(request, pk): 
    userForDeletion = User.objects.get(id=pk) 
    # admin user cannot be deleted directly  
    if(userForDeletion.is_staff):
        #return Response('Admin user cannot be deleted')
        return Response({'detail':'Admin user cannot be deleted'}, status=status.HTTP_400_BAD_REQUEST) 
    else: 
        userForDeletion.delete() # deleted any normal user 
        return Response('User was deleted')
