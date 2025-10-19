from django.urls import path
from . import dealer_views


urlpatterns = [
    path('dealer_register/', dealer_views.dealer_register, name='dealer_register'),
    path('dealer_dashboard/', dealer_views.dealer_dashboard, name='dealer_dashboard'),
]