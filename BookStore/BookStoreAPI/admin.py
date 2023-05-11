from django.contrib import admin
from BookStoreAPI.models import BookItem, BookCategory, Cart, CartItem, Order

admin.site.register(BookItem, BookCategory, Cart, CartItem, Order)
