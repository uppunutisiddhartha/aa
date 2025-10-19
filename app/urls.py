"""
URL configuration for Lastminuteai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('login/', views.rolelogin, name='rolelogin'),
    path('logout/', views.logout_view, name='logout'),
    path('customer_register/', views.customer_register, name='customer_register'),
]
