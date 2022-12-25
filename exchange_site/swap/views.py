import os
from pathlib import Path
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
import pymongo
import re
from bson.json_util import dumps, loads
import json
from bson.objectid import ObjectId
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, View, UpdateView, DeleteView
from django.views.generic.edit import DeletionMixin
from pymongo import TEXT
import datetime
from .forms import ImportOfferFromJSONForm, OfferForm, LoginForm, RegisterForm, EditOfferForm
from django.core.paginator import Paginator

BASE_DIR = Path(__file__).resolve().parent.parent

# Подключение к MongoClient
client = pymongo.MongoClient('mongo', 27017, username='admin', password='admin')
# Получаем базу данных
dbname = client['swap_db']
# Получаем коллекцию(аналог таблицы)
offers_collection = dbname['swap_collection']
# Таблица купленного
selled_offers_collection = dbname['selled_collection']

offers = [
  { "title": "Some title 1",
        "description": "Some description abc",
        "weight": "45",
        "size": "30",
        "category": "Мебель",
        "state": "Новое",
        "city": "Moscow",
        "price": "450",
        "created_at": "16-12-2022 20:18",
        "owner": "Bob",
        },
    {"title": "Some title 2",
     "description": "Some description zxc",
     "weight": "35",
     "size": "5",
     "category": "Мебель",
     "state": "Хорошее",
     "city": "Taganrog",
     "price": "120",
     "created_at": "16-12-2022 20:18",
     "owner": "Bob",
     },
    {"title": "Some title 3",
     "description": "Some description qwe",
     "weight": "77",
     "size": "51",
     "category": "Мебель",
     "state": "Новое",
     "city": "Moscow",
     "price": "150",
     "created_at": "16-12-2022 20:18",
     "owner": "Bob",
     },
    {"title": "Some title 4",
     "description": "Some description fgh",
     "weight": "70",
     "size": "51",
     "category": "Одежда",
     "state": "Новое",
     "city": "Belgorod",
     "price": "250",
     "created_at": "16-12-2022 20:18",
     "owner": "Bob",
     },
    {"title": "Some title 5",
     "description": "Some description opl",
     "weight": "71",
     "size": "51",
     "category": "Одежда",
     "state": "Хорошее",
     "city": "Belomorsk",
     "price": "250",
     "created_at": "16-12-2022 20:18",
     "owner": "Bob",
     },
    {"title": "Some title 6",
     "description": "Some description mhg",
     "weight": "73",
     "size": "51",
     "category": "Одежда",
     "state": "Среднее",
     "city": "Sarta",
     "price": "1590",
     "created_at": "16-12-2022 20:18",
     "owner": "Bob",
     },
    {"title": "Some title 7",
     "description": "Some description nmg",
     "weight": "55",
     "size": "30",
     "category": "Мебель",
     "state": "Новое",
     "city": "Moscow",
     "price": "450",
     "created_at": "16-12-2022 20:18",
     "owner": "Bob",
     },
]

users_collection = dbname['users_collection']
users_collection.create_index([('email', pymongo.ASCENDING)], unique=True)

offers_collection.insert_many(offers)

class HomeView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        dbname = client['swap_db']
        collection = dbname['swap_collection']
        context["offers"] = collection.find()
        offers = list(collection.find())
        paginator = Paginator(offers, 9)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class OfferView(TemplateView):
    template_name = "offer.html"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        context["offer"] = offers_collection.find_one({"_id": ObjectId(self.kwargs.get("slug"))})
        # context["can_write"] = self.request.user.username == context["offer"]
        context["id"] = self.kwargs.get("slug")
        return context


class Search(TemplateView):
    template_name = "search.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offers_collection.create_index([('title', TEXT)], default_language='english')
        print(self.request.GET.get('category'))
        if self.request.GET.get('category') == "Категория" and self.request.GET.get('state') == "Состояние":
            offers = offers_collection.find({
               "$and": [{"title": {"$regex": f".*{self.request.GET.get('title')}.*", "$options": 'i'}},
                       {"description": {"$regex": f".*{self.request.GET.get('description')}.*", "$options": 'i'}},
                        {"weight": {"$regex": f".*{self.request.GET.get('weight')}.*", "$options": 'i'}},
                        {"size": {"$regex": f".*{self.request.GET.get('size')}.*", "$options": 'i'}},
                        {"price": {"$regex": f".*{self.request.GET.get('price')}.*", "$options": 'i'}},
                       {"city": {"$regex": f".*{self.request.GET.get('city')}.*", "$options": 'i'}}]
            })
        elif self.request.GET.get('state') == "Состояние":
            offers = offers_collection.find({
                "$and": [{"title": {"$regex": f".*{self.request.GET.get('title')}.*", "$options": 'i'},
                         'category': f"{self.request.GET.get('category')}"},
                        {"description": {"$regex": f".*{self.request.GET.get('description')}.*", "$options": 'i'},
                         'category': f"{self.request.GET.get('category')}"},
                        {"weight": {"$regex": f".*{self.request.GET.get('weight')}.*", "$options": 'i'},
                         'category': f"{self.request.GET.get('category')}"},
                        {"size": {"$regex": f".*{self.request.GET.get('size')}.*", "$options": 'i'},
                         'category': f"{self.request.GET.get('category')}"},
                        {"price": {"$regex": f".*{self.request.GET.get('price')}.*", "$options": 'i'},
                         'category': f"{self.request.GET.get('category')}"},
                        {"city": {"$regex": f".*{self.request.GET.get('city')}.*", "$options": 'i'},
                         'category': f"{self.request.GET.get('category')}"}]})
        elif self.request.GET.get('category') == "Категория":
            offers = offers_collection.find({
                "$and": [{"title": {"$regex": f".*{self.request.GET.get('title')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}"},
                        {"description": {"$regex": f".*{self.request.GET.get('description')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}"},
                        {"weight": {"$regex": f".*{self.request.GET.get('weight')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}"},
                        {"size": {"$regex": f".*{self.request.GET.get('size')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}"},
                        {"price": {"$regex": f".*{self.request.GET.get('price')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}"},
                        {"city": {"$regex": f".*{self.request.GET.get('city')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}"}]})
        else:
            offers = offers_collection.find({
                "$and": [{"title": {"$regex": f".*{self.request.GET.get('title')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}",
                         'category': f"{self.request.GET.get('category')}"},
                        {"description": {"$regex": f".*{self.request.GET.get('description')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}",
                         'category': f"{self.request.GET.get('category')}"},
                        {"weight": {"$regex": f".*{self.request.GET.get('weight')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}",
                         'category': f"{self.request.GET.get('category')}"},
                        {"size": {"$regex": f".*{self.request.GET.get('size')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}",
                         'category': f"{self.request.GET.get('category')}"},
                        {"price": {"$regex": f".*{self.request.GET.get('price')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}",
                         'category': f"{self.request.GET.get('category')}"},
                        {"city": {"$regex": f".*{self.request.GET.get('city')}.*", "$options": 'i'},
                         'state': f"{self.request.GET.get('state')}",
                         'category': f"{self.request.GET.get('category')}"}]})

        
        paginator = Paginator(list(offers), 9)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        context["text"] = self.request.GET.get('category')
        context["full_path"] = re.sub(r"&+page=\d*", "", self.request.get_full_path())
        return context


class AddOfferView(FormView):
    template_name = "add_offer.html"
    form_class = OfferForm

    def form_valid(self, form):
        img = form.cleaned_data.get('photo')
        path = default_storage.save('tmp/somename.png', ContentFile(img.read()))
        offer = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        weight = str(form.cleaned_data.get('weight'))
        size = str(form.cleaned_data.get('size'))
        category = form.cleaned_data.get('category')
        state = form.cleaned_data.get('state')
        city = form.cleaned_data.get('city')
        price = str(form.cleaned_data.get('price'))
        offer_id = offers_collection.insert_one({'title': offer, 'description': description,
                                                 'weight': weight, 'size': size,
                                                 'category': category, 'state': state,
                                                 'city': city, 'price': price,
                                                 'created_at': datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                                                 'owner': self.request.user.username,
                                                 'photo': default_storage.url(path)}).inserted_id
        return redirect(reverse_lazy('offer', kwargs={'slug': offer_id}))

#this
class EditOfferView(FormView):
    template_name = "edit_offer.html"
    form_class = EditOfferForm

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        context["offer"] = offers_collection.find_one({"_id": ObjectId(self.kwargs.get("slug"))})
        # context["can_write"] = self.request.user.username == context["offer"]
        context["id"] = self.kwargs.get("slug")
        return context

    def form_valid(self, form):
        offer = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        weight = str(form.cleaned_data.get('weight'))
        size = str(form.cleaned_data.get('size'))
        category = form.cleaned_data.get('category')
        state = form.cleaned_data.get('state')
        city = form.cleaned_data.get('city')
        price = str(form.cleaned_data.get('price'))
        if form.cleaned_data.get('photo'):
            img = form.cleaned_data.get('photo')
            path = default_storage.save('tmp/somename.png', ContentFile(img.read()))
            offers_collection.update_one({"_id": ObjectId(self.kwargs.get("slug"))}, {'$set': {'title': offer, 'description': description,
                                                                                              'weight': weight, 'size': size,
                                                                                              'category': category, 'state': state,
                                                                                              'city': city, 'price': price,
                                                                                              'photo': default_storage.url(path)}})
        else:
            offers_collection.update_one({"_id": ObjectId(self.kwargs.get("slug"))},
                                         {'$set': {'title': offer, 'description': description,
                                                   'weight': weight, 'size': size,
                                                   'category': category, 'state': state,
                                                   'city': city, 'price': price,
                                                   }})

        return redirect(reverse_lazy('offer', kwargs={'slug': self.kwargs.get("slug")}))


class OfferJSONExportView(View):
    def get(self, request, *args, **kwargs):
        collection = dbname['swap_collection']
        offer = collection.find_one({"_id": ObjectId(self.kwargs.get("slug"))})
        json_str = dumps(offer, indent=4)
        response = HttpResponse(json_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=export.json' 
        return response


class BoughtOfferJSONExportView(View):
    def get(self, request, *args, **kwargs):
        collection = dbname['selled_collection']
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


class MyOffersJSONExportView(View):
    def get(self, request, *args, **kwargs):
        collection = dbname['swap_collection']
        offer = collection.find({"owner": self.request.user.username})
        json_str = dumps(offer, indent=4)
        response = HttpResponse(json_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=export.json'
        return response


class BoughtOffersJSONExportView(View):
    def get(self, request, *args, **kwargs):
        collection = dbname['selled_collection']
        offer = collection.find({"bought": self.request.user.username})
        json_str = dumps(offer, indent=4)
        response = HttpResponse(json_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=export.json'
        return response

class ImportOfferFromJSONView(View):
    form_class = ImportOfferFromJSONForm

    def post(self, request, *args, **kwargs):
        collection = dbname['swap_collection']
        file = request.FILES.getlist('file')[0]

        try:
            offer = loads(dumps(json.loads(file.read())))
        except json.JSONDecodeError as e:
            return render(
                request,
                template_name='error.html',
                context={
                    'error_code': 400, 
                    'error_message': 'Invalid JSON format'
                    }
                )

        print(offer, flush=True)

        if isinstance(offer, list):
            collection.insert_many(offer)
            return redirect(reverse_lazy('home'))
        else:
            offer_id = collection.insert_one(offer).inserted_id
            return redirect(reverse_lazy('offer', kwargs={'slug':offer_id}))
    
    
class Login(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):
        if users_collection.find_one({"email": form.cleaned_data.get('email'), 'password': form.cleaned_data.get('password')}):
            if User.objects.get(email=form.cleaned_data.get('email')):
                login(self.request, User.objects.get(email=form.cleaned_data.get('email')))
            else:
                login(self.request, User.objects.create_user(users_collection.find_one({"email": form.cleaned_data.get('email'), 'password': form.cleaned_data.get('password')}).full_name,
                                                             form.cleaned_data.get('email'),
                                                             form.cleaned_data.get('password')))
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


class UserOffers(TemplateView):
    template_name = "my_offers.html"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        context["offers"] = offers_collection.find({"owner": self.request.user.username})
        return context


class DeleteOfferView(View, DeletionMixin):
    def delete(self, request, *args, **kwargs):
        offers_collection.delete_one({"_id": ObjectId(self.kwargs.get("slug"))})
        return redirect(reverse_lazy('home'))


class BuyOfferView(View, DeletionMixin):
    def delete(self, request, *args, **kwargs):
        add = offers_collection.find_one({"_id": ObjectId(self.kwargs.get("slug"))})
        add.update({"bought": self.request.user.username})
        selled_offers_collection.insert_one(add)
        offers_collection.delete_one({"_id": ObjectId(self.kwargs.get("slug"))})
        return redirect(reverse_lazy('bought_offer', kwargs={'slug': ObjectId(self.kwargs.get("slug"))}))

class BoughtOffers(TemplateView):
    template_name = "bought_offers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["offers"] = selled_offers_collection.find({"bought": self.request.user.username})
        return context

class MyOfferView(TemplateView):
    template_name = "offer.html"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        context["offer"] = selled_offers_collection.find_one({"_id": ObjectId(self.kwargs.get("slug"))})
        # context["can_write"] = self.request.user.username == context["offer"]
        context["id"] = self.kwargs.get("slug")
        return context


class BoughtOfferView(TemplateView):
    template_name = "bought_offer.html"

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        context["offer"] = selled_offers_collection.find_one({"_id": ObjectId(self.kwargs.get("slug"))})
        # context["can_write"] = self.request.user.username == context["offer"]
        context["id"] = self.kwargs.get("slug")
        return context
