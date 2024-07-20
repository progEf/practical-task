
from rest_framework import serializers
from Search.models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'subject', 'lat', 'lon']