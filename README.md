# BookStore
A BookStore API built using Django REST framework that supports adding, listing books and categories,
adding books to cart, placing an order, and user permissions and group management.

# Install
- Clone the repo and create virtual env
- ```cd BookStore```
  ```pip install requirements.txt```
  ```cd BookStore```
  ```python3 manage.py makemigrations```
  ```python3 manage.py migrate```
- To load DB with initial book data \
  ```python3 manage.py loaddata ./BookStoreAPI/fixtures```
- Create superuser to access group management endpoints \
  ```python3 manage.py createsuperuser```
- Run the server and head to localhost \
  ```python3 manage.py runserver```

# API endpoints
## User registration
  POST method for all users
  ``` 
      /register          
      /login        
      /logout       
  ```
## Book and categories
  GET for users, ALL for manager 
  ``` 
      /books              
      /books/<id>       
      /categories       
      /categories/<id>  
  ```
## Cart
  ALL for users own cart items, ALL for manager all cart items
  ``` 
      /cart             
      /cart/<id>       
  ```
## Orders
  GET for users own orders, ALL for manager all orders, PATCH for carrier 
  ``` 
      /order             
      /order/<id>       
  ```
## Group management
  ALL for admin on manager endpoint, ALL for manager on carrier endpoint 
  ``` 
      /groups/manager             
      /groups/manager/<id>             
      /groups/carrier             
      /groups/carrier/<id>             
  ```
