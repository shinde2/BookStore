from rest_framework import serializers
from BookStoreAPI.models import BookItem, BookCategory
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


