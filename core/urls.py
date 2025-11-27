from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
