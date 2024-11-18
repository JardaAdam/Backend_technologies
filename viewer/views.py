from django.shortcuts import render

from viewer.models import Movie


def home(request):
    return render(request, "home.html")


def movies(request):
    # movies_list = Movie.objects.all()   """ vytahnu z databaze """
    # context = {'movies': movies_list}     """ vlozim do context """
    # return render(request, "movies.html", context)   """ pislu do templates movies.html """
    return render(request, "movies.html", {'movies': Movie.objects.all()})
