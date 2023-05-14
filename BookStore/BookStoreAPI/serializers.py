from rest_framework import serializers
from BookStoreAPI.models import BookItem, BookCategory, Cart, CartItem, Order
from BookStoreAPI.exceptions import UserNotFound404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime


class BookCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BookCategory
        fields = "__all__"


class BookItemSerializer(serializers.ModelSerializer):

    book_category = serializers.CharField(source="book_category.title", read_only=True)
    book_type = serializers.CharField(write_only=True)

    class Meta:
        model = BookItem
        fields = ["id", "title", "author", "price", "book_category", "book_type"]

    def create(self, validated_data):
        book_type = get_object_or_404(BookCategory, title=validated_data["book_type"])
        bookitem = BookItem.objects.create(
            title=validated_data["title"],
            author=validated_data["author"],
            price=validated_data["price"],
            book_category=book_type
        )
        bookitem.save()
        return bookitem


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["id", "username"]

    def validate_username(self, username):
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            raise UserNotFound404
        return username


class CartSerializer(serializers.ModelSerializer):

    bookitem = serializers.CharField(source="bookitem.title", read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    book = serializers.CharField(write_only=True)
    quantity = serializers.IntegerField(min_value=1, max_value=10, required=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "bookitem", "user", "book", "quantity", "price", "total"]

    def create(self, validated_data):
        user = User.objects.get(id=self.context["request"].user.id)
        bookitem = get_object_or_404(BookItem, title=validated_data["book"])
        cart = Cart.objects.create(
            user=user,
            bookitem=bookitem,
            quantity=validated_data["quantity"],
            price=bookitem.price,
            total=bookitem.price * validated_data["quantity"]
        )
        cart.save()
        return cart


class CartItemSerializer(serializers.ModelSerializer):

    order = serializers.CharField(source="order.id", read_only=True)
    bookitem = serializers.CharField(source="bookitem.title", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "order", "bookitem", "quantity", "price", "total"]
        read_only_fields = ["id", "quantity", "price", "total"]


class OrderSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source="user.username", read_only=True)
    carrier = serializers.CharField(source="carrier.username", read_only=True, allow_null=True)
    books = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "carrier", "status", "total", "date", "books"]
        read_only_fields = ["id", "status", "total", "date"]

    def get_books(self, order:Order):
        # queryset = order.cart_items.filter(order=order)
        # Use related name like above or below also works
        queryset = CartItem.objects.filter(order=order)
        return CartItemSerializer(queryset, many=True).data

    def create(self, validated_data):
        user = User.objects.get(id=self.context["request"].user.id)

        cart = Cart.objects.filter(user=user)
        if not cart:
            raise serializers.ValidationError(f"{user.username} does not have any books in cart")

        order = Order.objects.create(
            user=user,
            status=0,
            total=0,
            date=datetime.now()
        )
        order.save()

        total = 0
        for book in cart:
            cartitem = CartItem.objects.create(
                order=order,
                bookitem=book.menuitem,
                quantity=book.quantity,
                price=book.price,
                total=book.total
            )
            total += book.price
            cartitem.save()
        cart.delete()

        order.total = total
        order.save()

        return order
