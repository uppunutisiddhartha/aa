from django.urls import path
from . import dealer_views


urlpatterns = [
    path('dealer_register/', dealer_views.dealer_register, name='dealer_register'),
    path('dealer_dashboard/', dealer_views.dealer_dashboard, name='dealer_dashboard'),
     path('add-hotel/', dealer_views.add_hotel, name='add_hotel'),
    path('add-flight/', dealer_views.add_flight, name='add_flight'),
]