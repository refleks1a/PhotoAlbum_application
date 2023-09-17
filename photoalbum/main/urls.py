from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PhotoList.as_view(), name = 'gallery'),

    path('photo/<int:pk>/', PhotoDetail.as_view(), name = 'photo'),
    path('add/', AddPhoto, name = 'add'),
    path('delete/<int:pk>/', DeletePhoto.as_view(), name = 'delete'),
    path('update/<int:pk>/', UpdatePhoto.as_view(), name = 'update'),

    path('login/', LogIn.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page='login'), name = 'logout'),
    path('register/', Register.as_view(), name = 'register'),
]
