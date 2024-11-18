from django.shortcuts import render

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


def movie(request, pk):
    movie_ = Movie.objects.filter(id=pk)
    if movies:
        movie_ = movie_[0]
        context = {'movie': movie_}
        return render(request, "movie.html", context)
    return movies(request)  # osetreni co se stane kdyz film s hledanym nazvem neexistuje


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
