from django.urls import path 
from api.views import user_views as views


urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('register/', views.registerUser, name='register'),

    # update profile of logged in user, regular or admin 
    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"),
    
    # list of all users except logged in user 
    path('', views.getUsers, name="users"),

    # update user by id (except logged in user) 
    # these dynamic routes has to be placed at the lower section here 
    # in order to avoid possible conflict with 'profile' section routes 
    # if placed on top, the routing system may think 'profile' as a value for <str:pk> 
    path('<str:pk>/', views.getUserById, name="user-update-by-id"), 
    path('update/<str:pk>/', views.updateUser, name="user-update"),

    # delete user 
    path('delete/<str:pk>/', views.deleteUser, name='user-delete'),   
]

