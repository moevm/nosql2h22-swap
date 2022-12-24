from django import forms


class OfferForm(forms.Form):

    CATEGORY_CHOICES = [
        ('Мебель', 'Мебель'),
        ('Одежда', 'Одежда'),
        ('Бытовая техника', 'Бытовая техника'),
        ('Посуда', 'Посуда'),
        ('Продукты', 'Продукты'),
    ]

    STATE_CHOICES = [
        ('Новое', 'Новое'),
        ('Хорошее', 'Хорошее'),
        ('Среднее', 'Среднее'),
        ('Требует ремонта', 'Требует ремонта'),

    ]

    title = forms.CharField(label="Название", widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Описание", widget=forms.Textarea(attrs={"class": "form-control"}))
    photo = forms.ImageField()
    weight = forms.IntegerField(label="Вес", widget=forms.NumberInput(attrs={"class": "form-control"}))
    size = forms.IntegerField(label="Размер", widget=forms.NumberInput(attrs={"class": "form-control"}))
    category = forms.ChoiceField(label="Категория", choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    state = forms.ChoiceField(label="Состояние", choices=STATE_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    city = forms.CharField(label="Город", widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.IntegerField(label="Цена", widget=forms.NumberInput(attrs={"class": "form-control"}))

class ImportOfferFromJSONForm(forms.Form):
    file = forms.FileField(label='Файл')
    
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пороль", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пороль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    full_name = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": "form-control"}))

class EditOfferForm(forms.Form):

    CATEGORY_CHOICES = [
        ('Мебель', 'Мебель'),
        ('Одежда', 'Одежда'),
        ('Бытовая техника', 'Бытовая техника'),
        ('Посуда', 'Посуда'),
        ('Продукты', 'Продукты'),
    ]

    STATE_CHOICES = [
        ('Новое', 'Новое'),
        ('Хорошее', 'Хорошее'),
        ('Среднее', 'Среднее'),
        ('Требует ремонта', 'Требует ремонта'),

    ]

    title = forms.CharField(label="Название", widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="Описание", widget=forms.Textarea(attrs={"class": "form-control"}))
    photo = forms.ImageField(required=False)
    weight = forms.IntegerField(label="Вес", widget=forms.NumberInput(attrs={"class": "form-control"}))
    size = forms.IntegerField(label="Размер", widget=forms.NumberInput(attrs={"class": "form-control"}))
    category = forms.ChoiceField(label="Категория", choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    state = forms.ChoiceField(label="Состояние", choices=STATE_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))
    city = forms.CharField(label="Город", widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.IntegerField(label="Цена", widget=forms.NumberInput(attrs={"class": "form-control"}))
