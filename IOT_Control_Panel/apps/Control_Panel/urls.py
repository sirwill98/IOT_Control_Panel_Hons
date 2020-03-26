# pages/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('node', views.nodePageView, name='node'),
    path('register/', views.nodeRegisterView, name='node register'),
    path('gateway/', views.homePageView2, name='gatewayView'),
    path('nodeMapRegister/', views.nodeMapRegisterView, name='node map register')
]
