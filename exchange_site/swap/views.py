import os
from pathlib import Path
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
import pymongo
from bson.json_util import dumps, loads
import json
from bson.objectid import ObjectId
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, View
from pymongo import TEXT

from .forms import ImportOfferFromJSONForm, OfferForm, LoginForm, RegisterForm

BASE_DIR = Path(__file__).resolve().parent.parent

# Подключение к MongoClient
client = pymongo.MongoClient('mongo', 27017, username='admin', password='admin')
# Получаем базу данных
dbname = client['swap_db']
# Получаем коллекцию(аналог таблицы)
collection = dbname['swap_collection']

users_collection = dbname['users_collection']
users_collection.create_index([('email', pymongo.ASCENDING)], unique=True)

def index(request):

    message = [{"author": "Mike",
                  "text": "Another post!",
                  "title": "some text",
                  "tags": ["bulk", "insert"],
                  "date": "11:11:2011"},
                 {"author": "Eliot",
                  "title": "MongoDB is fun",
                  "text": "and pretty easy too!",
                  "date": "11:11:2011"}]

    collection.insert_many(message)

    return HttpResponse(str(collection.find()))


class HomeView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        dbname = client['swap_db']
        collection = dbname['swap_collection']
        context["offers"] = collection.find()
        return context



class OfferView(TemplateView):
    template_name = "offer.html"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        context["offer"] = collection.find_one({"_id": ObjectId(self.kwargs.get("slug"))})
        context["id"] = self.kwargs.get("slug")
        return context


class Search(TemplateView):
    template_name = "search.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection.create_index([('title', TEXT)], default_language='english')
        context["offers"] = collection.find({"$text": {"$search": f"{self.request.GET.get('search')}"}})
        context["text"] = self.request.GET.get('search')
        return context


class AddOfferView(FormView):
    template_name = "add_offer.html"
    form_class = OfferForm

    def form_valid(self, form):
        img = form.cleaned_data.get('photo')
        path = default_storage.save('tmp/somename.png', ContentFile(img.read()))

        offer = form.cleaned_data.get('title')
        offer_id = collection.insert_one({'title': offer, 'photo': default_storage.url(path)}).inserted_id
        return redirect(reverse_lazy('offer', kwargs={'slug': offer_id}))


class OfferJSONExportView(View):
    def get(self, request, *args, **kwargs):
        collection = dbname['swap_collection']
        offer = collection.find_one({"_id": ObjectId(self.kwargs.get("slug"))})
        json_str = dumps(offer, indent=4)
        response = HttpResponse(json_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=export.json' 
        return response

class OffersJSONExportView(View):
    def get(self, request, *args, **kwargs):
        collection = dbname['swap_collection']
        offer = collection.find({})
        json_str = dumps(offer, indent=4)
        response = HttpResponse(json_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=export.json' 
        return response


class ImportOfferFromJSONView(View):
    form_class = ImportOfferFromJSONForm

    def post(self, request, *args, **kwargs):
        collection = dbname['swap_collection']
        file = request.FILES.getlist('file')[0]
        offer = loads(dumps(json.load(file)))
        print(offer, flush=True)
        offer_id = collection.insert_one(offer).inserted_id
        return redirect(reverse_lazy('offer', kwargs={'slug':offer_id}))
    
    
class Login(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):
        if users_collection.find_one({"email": form.cleaned_data.get('email'), 'password': form.cleaned_data.get('password')}):
            login(self.request, User.objects.create_user('user', form.cleaned_data.get('email'), form.cleaned_data.get('password')))
        return redirect(reverse_lazy('home'))


class UserLogout(LogoutView):
    next_page = 'home'


class Register(FormView):
    template_name = "register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        users_collection.insert_one({'email': form.cleaned_data.get('email'),
                                     'password': form.cleaned_data.get('password'),
                                     'full_name': form.cleaned_data.get('full_name')})
        login(self.request, User.objects.create_user(form.cleaned_data.get('full_name'),
                                                     form.cleaned_data.get('email'),
                                                     form.cleaned_data.get('password')))
        return redirect(reverse_lazy('home'))
