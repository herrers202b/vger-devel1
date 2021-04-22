from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import include

from django.views.generic import RedirectView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.registerPage, name='register'),
    path('profile/', views.profilePage, name='profile'),
    path('accounts/login/', RedirectView.as_view(pattern_name='home-page')),
]
