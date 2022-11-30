import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from bson.objectid import ObjectId
from .forms import OfferForm
import pymongo
from  pymongo import TEXT
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# Подключение к MongoClient
client = pymongo.MongoClient('mongo', 27017, username='admin', password='admin')
# Получаем базу данных
dbname = client['swap_db']
# Получаем коллекцию(аналог таблицы)
collection = dbname['swap_collection']


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

