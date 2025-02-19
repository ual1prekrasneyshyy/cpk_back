from django.contrib.auth.views import LoginView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView, UserDetailView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('user', UserDetailView.as_view()),
    path('login', obtain_auth_token),
    path('logout', LogoutView.as_view()),
]