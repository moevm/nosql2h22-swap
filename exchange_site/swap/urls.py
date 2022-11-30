from django.contrib import admin
from django.urls import path, include
from .views import HomeView, OfferView, AddOfferView, Search, index, OfferJSONExportView, ImportOfferFromJSONView, OffersJSONExportView


urlpatterns = [
    path('', index),
    path('home/', HomeView.as_view(), name='home'),
    path('add_offer/', AddOfferView.as_view(), name='add_offer'),
    path('import_offer_from_json/', ImportOfferFromJSONView.as_view(), name='import_offer_from_json'),
    path('search/', Search.as_view(), name='search'),
    path('export_offers_to_json', OffersJSONExportView.as_view(), name='export_offers_to_json'),
    path('offer/<str:slug>/', OfferView.as_view(), name='offer'),
    path('offer/<str:slug>/export', OfferJSONExportView.as_view(), name='export_offer')
]
