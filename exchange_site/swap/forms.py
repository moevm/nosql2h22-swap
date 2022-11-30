from django import forms


class OfferForm(forms.Form):
    title = forms.CharField(label="Название", widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Описание", widget=forms.Textarea(attrs={"class": "form-control"}))
    photo = forms.ImageField(required=False)

    # weight = forms.CharField(label="Вес", widget=forms.TextInput(attrs={"class": "form-control"}))
    # size = forms.CharField(label="Габариты", widget=forms.TextInput(attrs={"class": "form-control"}))
    # category = forms.CharField(label="Категория", widget=forms.TextInput(attrs={"class": "form-control"}))
    # state = forms.CharField(label="Состояние", widget=forms.TextInput(attrs={"class": "form-control"}))
    # city = forms.CharField(label="Город", widget=forms.TextInput(attrs={"class": "form-control"}))
    # price = forms.IntegerField(label="Цена", widget=forms.NumberInput(attrs={"class": "form-control"}))

class ImportOfferFromJSONForm(forms.Form):
    file = forms.FileField(label='Файл')