from rest_framework import serializers
from .models import movies
class moviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = movies
        fields = ["title", "overview", "data_sources", "rate"]