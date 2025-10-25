
import requests

class MeteoApiHandler:
    """
        Handler that manages all queries to the Open Meteo Geocoding API and the data it receives.
    """
    def get_coordinates(self, city_name):
        """
            Obtains latitude and longitude by city name from API.
        :return:
        """
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city_name,
            "count": 1,  # solo la primera coincidencia
            "language": "es",
            "format": "json"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            lat = data["results"][0]["latitude"]
            lon = data["results"][0]["longitude"]
            return lat, lon
        else:
            raise ValueError(f"No se encontraron coordenadas para {city_name}")

    def get_weather_data(self, lat, lon, start_date, end_date):
        """
        Obtains weather data by latitude, longitude and dates interval from API.
        :param lon:
        :param start_date:
        :param end_date:
        :return:
        """
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["temperature_2m", "surface_pressure"],
            "timezone": "Europe/Madrid"
        }
        response = requests.get(url, params=params)
        data = response.json()
        return data
    # func: calcular estadisticas de temperatura
    # func: calcular estadisticas de precipitaciones
    # func: calcular estiadisticas generales (llamada a las dos anteriores)
