from django.db import models
from django.db.models import Model, CharField


# Create your models here.
# tabulka o dvou sloupcich
class Genre(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    """              delka, nesmi byt nevyplneno,nesmi byt prazdne pole pri odesilani formulare, unikatni   """