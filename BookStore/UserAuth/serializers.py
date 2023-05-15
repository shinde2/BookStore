from rest_framework import serializers
from BookStoreAPI.exceptions import UserNotFound404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {
            "username": {
                "required": True,
                "min_length": 4,
                "max_length": 8,
                "validators": [UniqueValidator(queryset=User.objects.all())]
            },
            "password": {
                "write_only": True,
            },
        }

    def validate_password(self, password):
        validate_password(password)
        return password
