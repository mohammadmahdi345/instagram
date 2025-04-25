from django.urls import path
from .views import *

urlpatterns = [

    path('users/', UserListView.as_view(), name='user-list'),
    path('request/<int:pk>/', RequestView.as_view(), name='request'),
    path('request-list/', RequestListView.as_view(), name='request-list'),
    path('accepted/<int:pk>/', AcceptView.as_view(), name='accepted'),
    path('fallowers/', FallowersUsersView.as_view(), name='fallower'),
    path('fallowing/', FallowingUsersView.as_view(), name='fallowing')
]