# pages/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('node', views.nodePageView, name='node'),
    path('register/<str:ip>/', views.nodeRegisterView, name='node register'),
    path('register/', views.nodePreegisterView, name='node preregister')
]
