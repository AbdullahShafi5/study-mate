from unicodedata import name
from urllib import request
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.register, name="register"),
    path("login/", views.LoginPage, name='login'),
    path("logout/", views.logoutUser, name="logout"),
    path('room/<int:pk>',views.room, name='room' ),
    path('create-room',views.create_room, name='create-room'),
    path('update-room/<int:pk>',views.update_room, name='update-room'),
    path('delete-room/<int:pk>',views.deleteRoom, name='delete-room'),
    path('delete-message/<int:pk>',views.deleteMessage, name='delete-message'),
    path('profile/<str:pk>',views.userProfile, name='user-profile'),
    
    
]
