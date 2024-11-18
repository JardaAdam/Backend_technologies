from django.shortcuts import render

from viewer.models import Movie


def home(request):
    return render(request, "home.html") # odkaz na statickou stranku


def movies(request):
    # movies_list = Movie.objects.all()   """ vytahnu z databaze """
    # context = {'movies': movies_list}     """ vlozim do context """
    # return render(request, "movies.html", context)   """ pislu do templates movies.html """
    return render(request, "movies.html", {'movies': Movie.objects.all()})

def movie(request, pk):
    if Movie.objects.filter(id=pk).exists():
        movie_ = Movie.objects.get(id=pk)
        context = {'movie': movie_}
        return render(request, "movie.html", context)
    return movies(request)  # osetreni co se stane kdyz film s hledanym nazvem neexistuje