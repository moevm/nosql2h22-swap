from django.contrib import admin
from django.urls import path, include
from .views import HomeView, OfferView, AddOfferView, Search, OfferJSONExportView, ImportOfferFromJSONView, OffersJSONExportView, Login, UserLogout, Register


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_offer/', AddOfferView.as_view(), name='add_offer'),
    path('import_offer_from_json/', ImportOfferFromJSONView.as_view(), name='import_offer_from_json'),
    path('search/', Search.as_view(), name='search'),
    path('export_offers_to_json', OffersJSONExportView.as_view(), name='export_offers_to_json'),
    path('offer/<str:slug>/', OfferView.as_view(), name='offer'),
    path('offer/<str:slug>/export', OfferJSONExportView.as_view(), name='export_offer'),
    path('login', Login.as_view(), name='login'),
    path('logout', UserLogout.as_view(), name='logout'),
    path('register', Register.as_view(), name='register'),
]
