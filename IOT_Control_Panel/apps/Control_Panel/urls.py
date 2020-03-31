# pages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('node/', views.nodePageView, name='node'),
    path('register/', views.nodeRegisterView, name='node register'),
    path('espregister/', views.nodeEspRegisterView, name='esp register'),
    path('esppreupdate/', views.nodeEspPreUpdateView, name='begin esp update'),
    path('espupdate/<int:ID>', views.nodeEspUpdateView, name='esp update'),
    path('gateway/', views.homePageView2, name='gatewayView'),
    path('nodeMapRegister/', views.nodeMapRegisterView, name='node map register'),
    path('deletenode/<int:ID>', views.deletenode, name='Delete Node'),
    path('reading/', views.readingPage, name='Latest Reading'),
    path('deletewaiting/<int:ID>', views.deletewaiting, name='Latest Reading'),
    path('waitingNodes/', views.waitingNodesView, name='Waiting Nodes')
]