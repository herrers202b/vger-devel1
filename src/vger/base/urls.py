from django.urls import path
from . import views

urlpatterns += [
    path('base/', include('base.urls')),
]