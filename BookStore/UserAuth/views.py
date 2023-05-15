from rest_framework import generics, status
from rest_framework.response import Response
from UserAuth.serializers import RegisterUserSerializer, LoginUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(**serializer.validated_data)
        user.set_password(serializer.validated_data.get("password"))
        user.save()
        return Response({"Success": f"{user.username} is registered."}, status=status.HTTP_200_OK)


class LogInUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user is None:
            return Response({"Error": "Invalid credentials provided."}, status=status.HTTP_401_UNAUTHORIZED)
        token, __ = Token.objects.get_or_create(user=user)
        return Response({"user": user.username, "token": token.key}, status=status.HTTP_200_OK)


class LogOutUser(generics.CreateAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"Success": f"{request.user.username} logged out."}, status=status.HTTP_200_OK)
