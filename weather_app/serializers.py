from rest_framework import serializers
from weather_app.models import Location, HourlyWeatherData

"""
Serializers are useful to convert models into JSON data. 
"""

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'

class HourlyWeatherDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = HourlyWeatherData
        fields = '__all__'
