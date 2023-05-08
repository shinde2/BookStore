from rest_framework import serializers
from BookStoreAPI.models import BookItem, BookCategory, Cart
from BookStoreAPI.exceptions import UserNotFound404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime


class BookCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BookCategory
        fields = "__all__"


class BookItemSerializer(serializers.ModelSerializer):

    book_category = serializers.CharField(source="category.title", read_only=True)
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


