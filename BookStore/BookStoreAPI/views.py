from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from BookStoreAPI.serializers import BookItemSerializer, BookCategorySerializer, UserSerializer
from BookStoreAPI.serializers import CartSerializer, OrderSerializer
from BookStoreAPI.models import BookItem, BookCategory, Cart, Order
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from BookStoreAPI.permissions import IsManager, IsCarrier
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from BookStoreAPI.exceptions import UserNotFound404, UserNotGroup404
from random import choice


class BookItemsList(generics.ListCreateAPIView):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
    ordering_fields = ["price"]
    search_fields = ["title", "book_category__title"]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [perm() for perm in self.permission_classes]


class BookItemsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [perm() for perm in self.permission_classes]


class BookCategoryList(generics.ListCreateAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
    search_fields = ["title"]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [perm() for perm in self.permission_classes]


class BookCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [perm() for perm in self.permission_classes]


class ManagersList(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]

    def post(self, request, *args, **kwargs):
        # use request.data for form data, kwargs for url parameters
        username = request.data.get("username")
        try:
            user = User.objects.get(username=username)
        except:
            raise UserNotFound404
        group = Group.objects.get(name="Manager")
        user.groups.add(group)
        # or this also works
        # group.user_set.add(user)
        return Response({"Success": f"{username} is now Manager"}, status=status.HTTP_200_OK)


class ManagersDetail(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs["pk"])
        except:
            raise UserNotFound404
        group = Group.objects.get(name="Manager")
        if group.user_set.filter(id=user.id).exists():
            user.groups.remove(group)
        else:
            raise UserNotGroup404
        user.groups.remove(group)
        return Response({"Success": f"{user.username} is removed from Manager"}, status=status.HTTP_200_OK)


class CarrierList(generics.CreateAPIView):
    queryset = User.objects.filter(groups__name="Carrier")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        try:
            user = User.objects.get(username=username)
        except:
            raise UserNotFound404
        group = Group.objects.get(name="Carrier")
        user.groups.add(group)
        return Response({"Success": f"{username} is now a Carrier"}, status=status.HTTP_200_OK)


class CarrierDetail(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name="Carrier")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsManager]

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs["pk"])
        except:
            raise UserNotFound404
        group = Group.objects.get(name="Carrier")
        if group.user_set.filter(id=user.id).exists():
            user.groups.remove(group)
        else:
            raise UserNotGroup404
        return Response({"Success": f"{user.username} is removed from Carrier"}, status=status.HTTP_200_OK)


class CartsList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class OrdersList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ["total"]
    search_fields = ["status"]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.groups.filter(name="Manager"):
            return Order.objects.all()
        elif self.request.user.groups.filter(name="Carrier"):
            return Order.objects.filter(carrier=self.request.user)
        else:
            return Order.objects.filter(user=self.request.user)


class OrdersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs["pk"])
        if request.user.is_staff or request.user.groups.filter(name="Manager") or order.user == request.user:
            return super().get(request, *args, **kwargs)
        else:
            return Response({"Forbidden": "Can not access this order"},
                            status=status.HTTP_403_FORBIDDEN)

    def order_update(self, request, *args, **kwargs):
        if self.request.user.groups.count() == 0:
            return Response({"Forbidden": "Can not update this order"},
                            status=status.HTTP_403_FORBIDDEN)

        order = get_object_or_404(Order, id=kwargs["pk"])

        # If carrier is null, pick a random carrier
        if not order.carrier and (request.user.is_staff or request.user.groups.filter(name="Manager")):
            try:
                carrier = choice(User.objects.filter(groups__name="Carrier"))
            except IndexError as e:
                return Response({"Not Found": "No carrier available"},
                                status=status.HTTP_404_NOT_FOUND)
            order.carrier = carrier
            order.save()

        # If carrier id is provided, then use that as new carrier person
        if request.user.is_staff or request.user.groups.filter(name="Manager"):
            if request.data.get("carrier", None):
                carrier = get_object_or_404(User, id=request.data.get("carrier"))
                if not carrier.groups.filter(name="Carrier"):
                    return Response({"Not Found": "Given user is not a carrier"},
                                    status=status.HTTP_404_NOT_FOUND)
                order.carrier = carrier
                order.save()

        stat = request.data.get("status", None)
        if stat:
            order.status = stat
            order.save()

        return Response({"Success": "Order updated successfully"},
                        status=status.HTTP_200_OK)

    # To update status, use multipart form data with "status" = 0/1/2
    # To update carrier, use multipart form data with "carrier" = id
    def put(self, request, *args, **kwargs):
        return self.order_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.order_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.groups.filter(name="Manager"):
            return super().delete(request, *args, **kwargs)
        else:
            return Response({"Forbidden": "Can not delete this order"},
                            status=status.HTTP_403_FORBIDDEN)
