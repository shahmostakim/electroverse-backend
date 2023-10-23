# Backend Project: Electroverse Backend API

This is one of the portfolio projects listed in my [website](https://shahmostakim.com).


## Project Description
This is the backend API for project: Electroverse. Built with Django REST, this API implements JWT authentication and role based authorization. 

The Project is deployed on EC2 instance maintaining CI/CD pipeline with GitHub, Jenkins and Docker

### List of some API endpoints:  

/api/products/
 - finds list of products 

/api/products/[id]/
 - gets detail information of a product specified by ID 

/api/products/add/
 - Adds new product (needs authorization) 

/api/products/update/[id]
 - Updates existing product specified by ID (needs authorization)

/api/products/delete/[id]
 - Deletes existing product specified by ID (needs authorization)  

/api/orders/
 - finds list of all customer orders (needs authorization)

/api/orders/add
 - Adds new order upon user checkout operation (needs authorization)

/api/orders/myorders
 - finds list of orders, for logged in user 

/api/orders/[id]
 - finds details about a single order, specified by order_ID

/api/orders/[id]/pay
 - processes payment for the order specified by ID (needs authorization) 

/api/users/login
 - Validates user credentials received from frontend part 

/api/users/register
 - New user registration 

/api/users/profile
 - shows user information for logged in user (needs authorization)

/api/users/profile/update
 - updates user information for logged in user (needs authorization)

/api/users/update/[id]/
 - Admin user modifies a regular user (activate/deactivate, make admin), (needs authorization)

/api/users/delete/[id]/
 - Admin user can delete a regular user specified by ID (needs authorization)

 
The API is under continuous development. More endpoints are added as the API improves 
