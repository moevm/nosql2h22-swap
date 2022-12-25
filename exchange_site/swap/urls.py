from django.contrib import admin
from django.urls import path, include
from .views import HomeView, MyOfferView, MyOffersJSONExportView, BoughtOffersJSONExportView, BoughtOfferJSONExportView, BoughtOfferView,  BuyOfferView, BoughtOffers, OfferView, AddOfferView, Search, OfferJSONExportView, ImportOfferFromJSONView, OffersJSONExportView, Login, UserLogout, Register, UserOffers, EditOfferView, DeleteOfferView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_offer/', AddOfferView.as_view(), name='add_offer'),
    path('buy_offer/<str:slug>/', BuyOfferView.as_view(), name='buy_offer'),
    path('edit_offer/<str:slug>/', EditOfferView.as_view(), name='edit_offer'),
    path('delete_offer/<str:slug>/', DeleteOfferView.as_view(), name='delete_offer'),
    path('import_offer_from_json/', ImportOfferFromJSONView.as_view(), name='import_offer_from_json'),
    path('search/', Search.as_view(), name='search'),
    path('my_offers/', UserOffers.as_view(), name='user_offers'),
    path('my_bought_offers/', BoughtOffers.as_view(), name='my_bought_offers'),
    path('export_offers_to_json', OffersJSONExportView.as_view(), name='export_offers_to_json'),
    path('export_my_offers_to_json', MyOffersJSONExportView.as_view(), name='export_my_offers_to_json'),
    path('export_bought_offers_to_json', BoughtOffersJSONExportView.as_view(), name='export_bought_offers_to_json'),
    path('offer/<str:slug>/', OfferView.as_view(), name='offer'),
    path('bought_offer/<str:slug>/', BoughtOfferView.as_view(), name='bought_offer'),
    path('my_offer/<str:slug>/', MyOfferView.as_view(), name='my_offer'),
    path('offer/<str:slug>/export', OfferJSONExportView.as_view(), name='export_offer'),
    path('bought_offer/<str:slug>/export', BoughtOfferJSONExportView.as_view(), name='bought_export_offer'),
    path('login', Login.as_view(), name='login'),
    path('logout', UserLogout.as_view(), name='logout'),
    path('register', Register.as_view(), name='register'),
]
