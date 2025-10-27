from django.urls import path
from .views import WeatherController

app_name = 'weather_app'
urlpatterns = [
    path('weather_data/', WeatherController.as_view(), name='weather_data'),
    path('temperature/', WeatherController.as_view(), {'type': 'temperature'}, name='temperature'),
    path('precipitation/', WeatherController.as_view(), {'type': 'precipitation'}, name='precipitation'),
    path('general_statistics/', WeatherController.as_view(), {'type': 'general_statistics'},
         name='general_statistics')
]
