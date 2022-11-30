from django.contrib import admin
from django.urls import path, include
from .views import HomeView, OfferView, AddOfferView, Search, index


urlpatterns = [
    path('', index),
    path('home/', HomeView.as_view(), name='home'),
    path('add_offer/', AddOfferView.as_view(), name='add_offer'),
    path('search/', Search.as_view(), name='search'),
    path('offer/<str:slug>/', OfferView.as_view(), name='offer'),
]
