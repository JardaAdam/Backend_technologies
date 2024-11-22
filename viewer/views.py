from django.db.models.expressions import result
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, FormView, UpdateView, DeleteView

from viewer.forms import CreatorForm, MovieForm
from viewer.models import Movie, Creator, Genre, Country


def home(request):
    return render(request, "home.html")

""" Movie"""
def movies(request):
    # movies_list = Movie.objects.all()   """ vytahnu z databaze """
    # context = {'movies': movies_list}     """ vlozim do context """
    # return render(request, "movies.html", context)   """ pislu do templates movies.html """
    return render(request,
                  "movies.html",
                  {'movies': Movie.objects.all(),
                   'genres': Genre.objects.all()})


# Class-based views
## View class ->
class MoviesView(View):
    def get(self, request):
        return render(request,
                      "movies.html",
                      {'movies': Movie.objects.all(),
                       'genres': Genre.objects.all()})


## TemplateView class
# nahrada za def movies pracuje rovnou s template ale pracuji s databazi rucne (extra_context)
class MoviesTemplateView(TemplateView):
    template_name = "movies.html"
    extra_context = {'movies': Movie.objects.all(), 'genres': Genre.objects.all()}


## ListView
# pracuji zde rovnou s template a modelem.
#je zde obecna promena (object_list)
# je slozitejsi do template posilat data z vice tabulek
# vhodne pro jednoduche seznami
class MoviesListView(ListView):
    # tato view neposílá do template informace o žánrech
    # lze to řešit metodou get_context_data -> tam můžu přidávat cokoliv
    template_name = "movies.html"
    model = Movie
    # pozor: do template se posílají data pod názvem 'object_list'
    # nebo můžu přejmenovat
    context_object_name = 'movies'


def movie(request, pk):
    movie_ = Movie.objects.filter(id=pk)
    if movies:
        movie_ = movie_[0]
        context = {'movie': movie_}
        return render(request, "movie.html", context)
    return movies(request)  # osetreni co se stane kdyz film s hledanym nazvem neexistuje

""" Vkladani """

class MovieCreateView(CreateView):
    template_name = "form.html"
    form_class = MovieForm
    success_url = reverse_lazy("movies")

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)

""" Uprava dat Filmu """
class MovieUpdateView(UpdateView):
    template_name = "form.html"
    form_class = MovieForm
    success_url = reverse_lazy("movies")
    model = Movie

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)

""" Mazani dat Filmu"""

class MovieDeleteView(DeleteView):
    template_name = "confirm_delete.html"
    model = Movie
    success_url = reverse_lazy("movies")


""" Creator"""
# nahrada za def creators
class CreatorsListView(ListView):
    template_name = "creators.html"
    model = Creator


def creator(request, pk):
    try:
        # creator_ = Creator.objects.get(id=pk)  # pk = primari key
        # context = {'creator': creator_}
        # return render(request, "creator.html", context)
        return render(request, "creator.html", {'creator': Creator.objects.get(id=pk)})
    except:
        return home(request)

## Formulare
# pouzivaji se pro uzivatelskou praci s daty
# najdu v form.py

""" Vkladani """
class CreatorFormView(FormView):
    template_name = "form.html"
    form_class = CreatorForm  # odkazuje se na forms.py CreatorForm(ModelForm)
    success_url = reverse_lazy('creators')  # po ulozeni formulare se stranka vrati na adresu definovanou v urls.py

    # ulozeni dat od uzivatele ve formulari
    def form_valid(self, form):
        print("Form is valid")
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Creator.objects.create(             # touto funkci vytahnu data z formulare a vlozim je do databaze
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            date_of_birth=cleaned_data['date_of_birth'],
            date_of_death=cleaned_data['date_of_death'],
            nationality=cleaned_data['nationality'],
            biography=cleaned_data['biography'],
        )
        return result
    # tato funkce vypisuje chybovou hlasku pokud nejsou data zadana spravne
    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)

# zjednoduseny zapis predesle class cerpa data z models.py
# pokud upravuji v models.py nejake data u Model propise se mi to v cele funkcnosti kodu napr. upravi se struktura formulare
class CreatorCreateView(CreateView):
    template_name = "form.html"
    form_class = CreatorForm        # forms.py
    success_url = reverse_lazy('creators')  # presmerovava po odeslani formulare na zadanou url

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)

""" Uprava dat"""
class CreatorUpdateView(UpdateView):    # musim pridat url do urls.py
    template_name = "form.html"
    form_class = CreatorForm
    success_url = reverse_lazy('creators')
    model = Creator



    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)

""" Mazani dat """
class CreatorDeleteView(DeleteView):
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('creators')
    model = Creator



def genre(request, pk):
    try:
        return render(request, "genre.html", {'genre': Genre.objects.get(id=pk)})
    except:
        return home(request)


def country(request, pk):
    try:
        return render(request, "country.html", {'country': Country.objects.get(id=pk)})
    except:
        return home(request)
# TODO tato funkce funguje pouze pro filmy ale ne pro Actors!!
