from django.contrib import admin
from BookStoreAPI.models import BookItem, BookCategory, Cart, CartItem, Order

admin.site.register(BookItem)
admin.site.register(BookCategory)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
