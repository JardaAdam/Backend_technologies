from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Avg, Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, FormView, UpdateView, DeleteView

from accounts.models import Profile
from viewer.forms import CreatorForm, MovieForm, GenreModelForm, CountryModelForm, ReviewModelForm
from viewer.models import Movie, Creator, Genre, Country, Review


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
def get(request):
    return render(request,
                  "movies.html",
                  {'movies': Movie.objects.all(),
                   'genres': Genre.objects.all()})


class MoviesView(View):
    pass


## TemplateView class
# nahrada za def movies pracuje rovnou s template ale pracuji s databazi rucne (extra_context)
class MoviesTemplateView(TemplateView):
    template_name = "movies.html"
    extra_context = {'genres': Genre.objects.all()}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Načtení filmů s jejich průměrným hodnocením a počtem recenzí
        movies_avg_count = Movie.objects.annotate(avg_rating=Avg('reviews__rating'),
                                                  review_count=Count('reviews'))

        # Přidání dat do kontextu
        context['movies'] = movies_avg_count
        context['genres'] = Genre.objects.all()
        return context


## ListView
# pracuji zde rovnou s template a modelem.
# je zde obecna promena (object_list)
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


class MovieTemplateView(TemplateView):
    template_name = "movie.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        movie_ = Movie.objects.filter(id=pk)
        if movie_:
            context['movie'] = movie_[0]
            context['form_review'] = ReviewModelForm
            rating_avg = movie_[0].reviews.aggregate(Avg('rating'))['rating__avg']
            """ reviews -> related_name z class Review (Avg( cerpam z class Review)[klic ktery vraci hodnotu ze slovniku]                                                        """
            # print(f"rating_avg: {rating_avg}")
            context['rating_avg'] = rating_avg
            return context
        return reverse_lazy('movies')  # fixme branche dev commit Fixed redirect in case

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        reviews = Review.objects.filter(movie=context['movie'],
                                        reviewer=Profile.objects.get(user=request.user))
        if reviews.exists():
            review_ = reviews[0]
            review_.rating = request.POST.get('rating')
            review_.comment = request.POST.get('comment')
            review_.save()
        else:
            Review.objects.create(
                movie=context['movie'],
                reviewer=Profile.objects.get(user=request.user),
                rating=request.POST.get('rating'),
                comment=request.POST.get('comment')
            )
        movie_ = context['movie']
        rating_avg = movie_.reviews.aggregate(Avg('rating'))['rating__avg']
        # print(f"rating_avg: {rating_avg}")
        context['rating_avg'] = rating_avg
        return render(request, 'movie.html', context)


""" Vkladani """


class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = "form.html"
    form_class = MovieForm
    success_url = reverse_lazy("movies")
    permission_required = 'viewer.add_movie'

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)


""" Uprava dat Filmu """


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "form.html"
    form_class = MovieForm
    success_url = reverse_lazy("movies")
    model = Movie
    permission_required = 'viewer.change_movie'

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)


""" Mazani dat Filmu"""


class MovieDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "confirm_delete.html"
    model = Movie
    success_url = reverse_lazy("movies")
    permission_required = 'viewer.delete_movie'


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
    except Creator.DoesNotExist:
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
        Creator.objects.create(  # touto funkci vytahnu data z formulare a vlozim je do databaze
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
class CreatorCreateView(PermissionRequiredMixin, CreateView):
    template_name = "form.html"
    form_class = CreatorForm  # forms.py
    success_url = reverse_lazy('creators')  # presmerovava po odeslani formulare na zadanou url
    permission_required = 'viewer.add_creator'

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)


""" Uprava dat"""


class CreatorUpdateView(PermissionRequiredMixin, UpdateView):  # musim pridat url do urls.py
    template_name = "form.html"
    form_class = CreatorForm
    success_url = reverse_lazy('creators')
    model = Creator
    permission_required = 'viewer.change_creator'

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)


""" Mazani dat """


class CreatorDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('creators')
    model = Creator
    permission_required = 'viewer.delete_creator'


def genre(request, pk):
    try:
        return render(request, "genre.html", {'genre': Genre.objects.get(id=pk)})
    except Creator.DoesNotExist:
        return home(request)


class GenreCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = GenreModelForm
    success_url = reverse_lazy('home')
    permission_required = 'viewer.add_genre'

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)


class GenreUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = GenreModelForm
    success_url = reverse_lazy('home')
    model = Genre
    permission_required = 'viewer.change_genre'

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)


class GenreDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "confirm_delete.html"
    model = Genre
    success_url = reverse_lazy('home')
    permission_required = 'viewer.delete_genre'


class CountryCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('home')
    permission_required = 'viewer.add_country'

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)


class CountryUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('home')
    model = Country
    permission_required = 'viewer.change_country'

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)


class CountryDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "confirm_delete.html"
    model = Country
    success_url = reverse_lazy('home')
    permission_required = 'viewer.delete_country'


def country(request, pk):
    try:
        return render(request, 'country.html', {'country': Country.objects.get(id=pk)})
    except Creator.DoesNotExist:
        return home(request)
