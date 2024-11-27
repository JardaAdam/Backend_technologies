from datetime import date

from django.db.models import Model, CharField, DateField, ForeignKey, SET_NULL, TextField, IntegerField, \
    ManyToManyField, DateTimeField, CASCADE

from accounts.models import Profile
# Create your models here.
# tabulka o dvou sloupcich
class Genre(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    """              delka, nesmi byt nevyplneno,nesmi byt prazdne pole pri odesilani formulare, unikatni   """

    class Meta:
        """ tato trida meni usporadani podle jmena abecedne pro zobrazeni v """
        ordering = ['name']

    def __repr__(self):
        return f"Genre(name={self.name})"

    def __str__(self):
        return f"{self.name}"


class Country(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Countries"

    def __repr__(self):
        return f"Country(name={self.name})"

    def __str__(self):
        return self.name


class Creator(Model):
    first_name = CharField(max_length=32, null=True, blank=True)
    last_name = CharField(max_length=32, null=True, blank=True)
    date_of_birth = DateField(null=True, blank=True)
    date_of_death = DateField(null=True, blank=True)
    nationality = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL, related_name='creators_nationality')
    """                           po vymazani zeme je nastavi prazdna kolonka, pristup k seznamu hercu z dane zeme"""
    biography = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name','last_name', 'date_of_birth']

    def __repr__(self):
        return f"Creator(first_name=({self.first_name}, last_name={self.first_name}, date_of_birth={self.date_of_birth})"

    def __str__(self):
        return f"{self.first_name} {self.last_name} *({self.date_of_birth})"
        # "Martin Novák (1975-05-06)"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def age(self):
        end_date = self.date_of_death if self.date_of_death else date.today()

        age = end_date.year - self.date_of_birth.year - (
                (end_date.month, end_date.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age





class Movie(Model):
    title_orig = CharField(max_length=64, null=False, blank=False)
    title_cz = CharField(max_length=64, null=True, blank=True)
    year = IntegerField(null=True, blank=True)
    length = IntegerField(null=True, blank=True)
    directors = ManyToManyField("viewer.Creator", blank=True, related_name='directing')
    actors = ManyToManyField("viewer.Creator", blank=True, related_name='acting')
    """ odkazuje na tabulku ktera je vytvorena az po teto tabulce"""
    countries = ManyToManyField(Country, blank=True, related_name='movies')
    genres = ManyToManyField(Genre, blank=True, related_name='movies')
    description = TextField(blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title_orig']

    def __repr__(self):
        return f"Movie(title_orig={self.title_orig})"

    def __str__(self):
        return f"{self.title_orig} ({self.year})"

    def length_format(self):
        # Kontrola, zda je `self.length` definována a je to platná hodnota
        if not self.length:
            return "Neznámá délka"  # Nebo jakákoliv jiná výchozí hodnota
        hours = self.length // 60
        minutes = self.length % 60
        if minutes < 10:
            minutes = f"0{minutes}"
        return f"{hours}:{minutes}"


class Review(Model):
    movie = ForeignKey(Movie, on_delete=CASCADE, null=False, blank=False, related_name='reviews')
    reviewer = ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=False, related_name='reviews')
    rating = IntegerField(null=True, blank=True)  # 1-10
    comment = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated']
    def __repr__(self):
        return (f"Review(movie={self.movie}, reviewer={self.reviewer}, "
                f"rating={self.rating}, comment={self.comment})")
    def __str__(self):
        return (f"Reviewer: {self.reviewer}, movie: {self.movie}, rating={self.rating}, "
                f"comment: {self.comment[:50]}")