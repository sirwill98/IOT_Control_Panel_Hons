# pages/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('node', views.nodePageView, name='node')
]