from django.urls import path
from .views import RegisterView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
     path('listusers/', UserListView.as_view(), name='user-list'),
]
