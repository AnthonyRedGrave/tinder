from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('registration-2/', RegisterInfoView.as_view(), name='registration-2'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page = '/'), name = 'logout'),
]