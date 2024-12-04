import re
from datetime import date
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.expressions import result
from django.forms import Form, CharField, DateField, ModelChoiceField, Textarea, ModelForm, NumberInput, IntegerField

from viewer.models import Country, Creator, Movie, Genre, Review, Image


# pozor z ceho importuji!! zde importuji z django.form!!
# formular pro tvurce pomoci teto definice se nam automaticky vygeneruje formular.html

class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

        help_texts = {
            'description': "Zde zadejte text k filmu."
        }
        error_messages = {

        }

    """ Ošetření zapisu"""

    def clean_title_orig(self):
        initial = self.cleaned_data['title_orig']
        result = initial
        if initial:
            result = initial.title()
        return result

    def clean_title_cz(self):
        initial = self.cleaned_data['title_cz']
        result = initial
        if initial:
            result = initial.title()
        return result

    def clean_year(self):
        initial = self.cleaned_data['year']
        result = initial
        if initial and initial > date.today().year:
            raise ValidationError(" Film nemůže být natočen v budoucnu!!")
        return result

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)


"""
# tento formular neni vhodny pro rozvijejici se aplikace 
class CreatorForm(Form):
    first_name = CharField(max_length=32, required=False)
    last_name = CharField(max_length=32, required=False)
    date_of_birth = DateField(required=False)
    date_of_death = DateField(required=False)
    nationality = ModelChoiceField(queryset=Country.objects, required=False)
    biography = CharField(widget=Textarea, required=False)
"""


# tato class cerpa rovnou z modelu a upravy delam pouze na jednom miste a to v models.py
class CreatorForm(ModelForm):
    class Meta:
        model = Creator  # odkazuje se do models.py na class Creator(Model)
        fields = '__all__'
        # fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'biography']
        # exclude = ['nationality']

        help_texts = {
            'biography': "Zde zadejte biografii tvůrce."
        }
        error_messages = {
            # TODO
        }

    # first_name = CharField(max_length=32, required=False)
    # last_name = CharField(max_length=32, required=False)
    date_of_birth = DateField(required=False, widget=NumberInput(attrs={'type': 'date'}), label='Datum narození')
    date_of_death = DateField(required=False, widget=NumberInput(attrs={'type': 'date'}), label='Datum umrtí')
    # nationality = ModelChoiceField(queryset=Country.objects, required=False)
    # biography = CharField(widget=Textarea, required=False)
    """ Tento kód zajišťuje, že všechna viditelná pole formuláře budou mít přidanou CSS třídu form-control """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            # TODO pochopit co to dela

    # funkce pro kontrolu vlozenych dat a jejich uprava

    # pro jednu polozku
    # osetruje velke pismeno -> i kdyz uzivatel zada male prvni pismeno upravi e na velke
    def clean_first_name(self):
        initial = self.cleaned_data['first_name']
        print(f"initial: {initial}")
        result = initial  # pokud je pole prazdne vipise None
        if initial:
            result = initial.capitalize()
            print(f"result: {result}")
        return result

    def clean_last_name(self):
        """ Upraví zadané příjmení tak, aby začínalo velkým písmenem. """
        initial = self.cleaned_data['last_name']
        print(f"Initial = '{initial}'")
        result = initial
        if initial:
            result = initial.capitalize()
            print(f"result  = '{result}'")
        return result

    def clean_date_of_birth(self):
        initial = self.cleaned_data['date_of_birth']
        if initial and initial >= date.today():  # pokud je datum zadane a je vjetsi nebo rovne aktualnimu datu
            raise ValidationError(" Nelze zadavat datum v budoucnosti")
        return initial

    def clean_date_of_death(self):
        initial = self.cleaned_data['date_of_death']
        if initial and initial >= date.today():
            raise ValidationError(" Nelze zadavat datum v budoucnosti")
        return initial

    def clean_biography(self):
        # Force each sentence of the biography to be capitalized.
        initial = self.cleaned_data['biography']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    # funkce ktera pracuje s vice polozkami najednou
    # osetruje povinost zadat minimalne jedno jmeno
    def clean(self):
        cleaned_data = super().clean()  # vicistim si data pred spustenim funkce.
        initial_first_name = cleaned_data['first_name']
        initial_last_name = cleaned_data['last_name']
        if not initial_first_name and not initial_last_name:
            raise ValidationError(" Je potreba zadat minimalne jedno jmeno ")
        # porovnava datum narozeni a umrti
        initial_date_of_birth = cleaned_data.get('date_of_birth')
        initial_date_of_death = cleaned_data.get('date_of_death')
        if initial_date_of_birth and initial_date_of_death and initial_date_of_death <= initial_date_of_birth:
            raise ValidationError(" nelze umrit pred narozenim :)")

        return self.cleaned_data


class GenreModelForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            name = name.strip()
            name = name.capitalize()
        return name


class CountryModelForm(ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            name = name.strip()
            name = name.capitalize()
        return name


class MovieModelForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title_orig', 'title_cz', 'year', 'length', 'directors', 'actors', 'countries', 'genres',
                  'description']
        labels = {
            'title_orig': 'Originální název',
            'title_cz': 'Český název',
            'year': 'Rok',
            'length': 'Délka (min)',
            'directors': 'Režie',
            'actors': 'Herecké obsazení',
            'countries': 'Země',
            'genres': 'Žánry',
            'description': 'Popis',
        }
        help_texts = {
            'title_orig': 'Zadajte originální název filmu.',
            'title_cz': 'Zadajte český název filmu (pokud existuje).',
            'year': 'Zadajte rok vydání filmu.',
            'length': 'Délka filmu v minutách.',
            'description': 'Popis filmu, stručný obsah nebo jiné detaily.',
        }
        error_messages = {
            'title_orig': {
                'required': 'Tento údaj je povinný.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_title_orig(self):
        title_orig = self.cleaned_data['title_orig']
        if title_orig:
            title_orig = title_orig.strip()
            title_orig = title_orig.capitalize()
        return title_orig

    def clean_title_cz(self):
        title_cz = self.cleaned_data['title_cz']
        if title_cz:
            title_cz = title_cz.strip()
            title_cz = title_cz.capitalize()
        return title_cz

    def clean_year(self):
        year = self.cleaned_data['year']
        if year and year > date.today().year:
            raise ValidationError("Rok filmu nemůže být v budoucnosti.")
        return year

    def clean_length(self):
        length = self.cleaned_data['length']
        if length and length <= 0:
            raise ValidationError("Déžka filmu musí být větší než 0.")
        return length

    def clean(self):
        cleaned_data = super().clean()
        title_orig = cleaned_data.get('title_orig')
        if not title_orig:
            raise ValidationError("Originální název je povinný.")
        return cleaned_data


class ReviewModelForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Hodnocení',
            'comment': 'Komentář'
        }
    rating = IntegerField(min_value=1, max_value=10)



class ImageModelForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
        labels = {
            'image': 'Obrázek',
            'movie': 'Film',
            'actors': 'Herci',
            'description': 'Popis'
        }