# from django.http import HttpResponse
# import pymongo
from django.views.generic import TemplateView
# client = pymongo.MongoClient('mongo', 27017, username='admin', password='admin')


# def index(request):
#     dbname = client['swap_db']

#     collection = dbname['swap_collection']

#     message = {
#         "message": "Hello from db"
#     }

#     collection.insert_one(message)

#     return HttpResponse(str(collection.find()[0]))

class HomeView(TemplateView):
    template_name = "home.html"


class OfferView(TemplateView):
    template_name = "offer.html"
