from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from viewer.models import Movie, Creator, Genre, Country


def home(request):
    return render(request, "home.html")


def movies(request):
    # movies_list = Movie.objects.all()   """ vytahnu z databaze """
    # context = {'movies': movies_list}     """ vlozim do context """
    # return render(request, "movies.html", context)   """ pislu do templates movies.html """
    return render(request,
                  "movies.html",
                  {'movies': Movie.objects.all(),
                   'genres': Genre.objects.all()})


# Class-based views
## View class
class MoviesView(View):
    def get(self, request):
        return render(request,
                      "movies.html",
                      {'movies': Movie.objects.all(),
                       'genres': Genre.objects.all()})


## TemplateView class
# nahrada za def movies
class MoviesTemplateView(TemplateView):
    template_name = "movies.html"
    extra_context = {'movies': Movie.objects.all(), 'genres': Genre.objects.all()}


## ListView
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
