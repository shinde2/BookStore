from django.urls import path
from UserAuth import views


urlpatterns = [
    path('register', views.RegisterUser.as_view()),
    path('login', views.LoginUser.as_view()),
]
