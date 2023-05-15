from django.urls import path
from UserAuth import views


urlpatterns = [
    path('register', views.RegisterUser.as_view()),
    path('login', views.LogInUser.as_view()),
    path('logout', views.LogOutUser.as_view()),
]
