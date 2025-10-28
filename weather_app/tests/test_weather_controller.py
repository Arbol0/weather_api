from django.test import TestCase, Client
from datetime import datetime
from weather_app.models import Location, HourlyWeatherData
import json

class WeatherAppViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(locality="Madrid", lat=40.4168, long=-3.7038)
        HourlyWeatherData.objects.create(
            temperature=25.0,
            precipitation=0.3,
            date=datetime(2025, 10, 1, 12, 0),
            location=self.location
        )

    def test_weather_data_post(self):
        url = r"http://localhost:8000/weather_app/weather_data/"
        data = {"start_date": "2025-10-01", "end_date": "2025-10-01", "city_name": "Madrid"}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_general_statistics_get(self):
        url = r"http://localhost:8000/weather_app/general_statistics/"
        data = {"start_date": "2025-10-01", "end_date": "2025-10-01",
                "city_name": "Madrid", "threshold_high": 30, "threshold_low": 0}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, 200)
