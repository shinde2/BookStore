from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from UserAuth.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, AllowAny
from rest_framework.throttling import AnonRateThrottle
from BookStoreAPI.permissions import IsManager, IsCarrier
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from BookStoreAPI.exceptions import UserNotFound404, UserNotGroup404


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True):
        user = User(**serializer.validated_data)
        user.set_password(serializer.validated_data.get("password"))
        user.save()
        return Response({"Success": f"{user.username} is registered."}, status=status.HTTP_200_OK)
