from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user-update/', UserView.as_view(), name='user-update'),
    path('change-password/', UpdateUserPasswordView.as_view(), name='change-password'),
    path('ban-user/<int:pk>/', BanUserView.as_view(), name='ban-user'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/', UserProfileGetView.as_view(), name='user-profile2'),


]
