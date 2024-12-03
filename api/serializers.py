from rest_framework import serializers

from viewer.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title_orig', 'title_cz', 'year']