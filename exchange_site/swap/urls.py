from django.contrib import admin
from django.urls import path, include
# from .views import index
from .views import HomeView, OfferView


urlpatterns = [
    # path('', index),
    path('', HomeView.as_view(), name='home'),
    path('offer/', OfferView.as_view(), name='offer'),
]
