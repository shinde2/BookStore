from rest_framework import serializers
from BookStoreAPI.exceptions import UserNotFound404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {
            "username": {
                "required": True,
                "min_length": 4,
                "max_length": 20,
                "validators": [UniqueValidator(queryset=User.objects.all())]
            },
            "password": {
                "required": True,
                "write_only": True,
            },
        }

    def validate_password(self, password):
        validate_password(password)
        return password


# IMP: Note that we can not use model serializer here.
#      Model Serializer will check for username to be
#      unique as defined by Django AbstractUser, 
#      and will not let registered users login.
class LoginUserSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()
