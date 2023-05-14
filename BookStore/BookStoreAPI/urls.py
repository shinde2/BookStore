from django.urls import path
from BookStoreAPI import views


urlpatterns = [
    path('books', views.BookItemsList.as_view()),
    path('books/<int:pk>', views.BookItemsDetail.as_view()),
    path('categories', views.BookCategoryList.as_view()),
    path('categories/<int:pk>', views.BookCategoryDetail.as_view()),
    path('orders', views.OrdersList.as_view()),
    path('orders/<int:pk>', views.OrdersDetail.as_view()),
    path('cart/books', views.Carts.as_view()),
    path('groups/manager/users', views.ManagersList.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagersDetail.as_view()),
    path('groups/carrier/users', views.CarrierList.as_view()),
    path('groups/carrier/users/<int:pk>', views.CarrierDetail.as_view()),
]
