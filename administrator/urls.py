from django import views
from django.urls import path
from . import views

app_name = 'administrator'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('shop/', views.shop, name='shop'),
    path('listUsers/', views.listUsers, name='listUsers'),
    path('listCardProducts/', views.listCardProducts, name='listCardProducts'),
    path('listCards/', views.listCards, name='listCards'),
    path('createUser/', views.createUser, name='createUser'),
    path('createCardProduct/', views.createCardProduct, name='createCardProduct'),
    path('createCard/', views.createCard, name='createCard'),
]