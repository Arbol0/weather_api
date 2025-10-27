
import requests
import pandas as pd
import numpy as np
from weather_app.models import Location

class MeteoApiHandler:
    """
        Handler that manages all queries to the Open Meteo Geocoding API and the data it receives.
    """

    def __init__(self, messages: list):
        self.messages = messages

    def get_coordinates(self, city_name):
        """
        Obtains latitude and longitude by city name from API.
        :param city_name:
        :return:
        """
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city_name,
            "count": 1,  # only first coincidence
            "language": "es",
            "format": "json"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            coordinates = dict()
            coordinates['lat']: float = data["results"][0]["latitude"]
            coordinates['lon']: float = data["results"][0]["longitude"]
            return coordinates
        else:
            self.messages.append(f"No se encontraron coordenadas para {city_name}")
            coordinates = dict()
            coordinates['lat'] = None
            coordinates['lon'] = None
            return None

    def get_hourly_weather_data(self, latitude, longitude, start_date, end_date):
        """
        Obtains hourly weather data by latitude, longitude and dates interval from API.
        :param latitude:
        :param longitude:
        :param start_date:
        :param end_date:
        :return:
        """
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["temperature_2m", "precipitation"],
            "timezone": "Europe/Madrid"
        }
        response = requests.get(url, params=params)
        data = response.json()
        temperatures = data['hourly']['temperature_2m']
        precipitations = data['hourly']['precipitation']
        times = data['hourly']['time']
        return temperatures, precipitations, times

    def calculate_temperature_statistics(self, weather_data, threshold_high: float, threshold_low: float):
        """
        Calculates all temperature statistics from database weather data
        :param weather_data:
        :param threshold_high:
        :param threshold_low:
        :return:
        """
        df_weather = pd.DataFrame(list(weather_data))
        # Average temperature
        avg_temp = df_weather['temperature'].mean()
        # Maximum and minimum
        max_row = df_weather.loc[df_weather['temperature'].idxmax()]
        min_row = df_weather.loc[df_weather['temperature'].idxmin()]
        # Daily average
        df_weather['day'] = df_weather['date'].dt.date
        avg_by_day = df_weather.groupby('day')['temperature'].mean().to_dict()
        avg_by_day = {d.strftime('%Y-%m-%d'): v for d, v in avg_by_day.items()}
        # hours above or below threshold
        hours_above = np.sum(df_weather['temperature'] > threshold_high)
        hours_below = np.sum(df_weather['temperature'] < threshold_low)

        temperature_data = {
            "temperature": {
                "average": round(avg_temp, 1),
                "average_by_day": avg_by_day,
                "max": {
                    "value": round(max_row['temperature'], 1),
                    "date_time": max_row['date'].isoformat(timespec='minutes')
                },
                "min": {
                    "value": round(min_row['temperature'], 1),
                    "date_time": min_row['date'].isoformat(timespec='minutes')
                },
                "hours_above_threshold": int(hours_above),
                "hours_below_threshold": int(hours_below)
            }
        }
        return temperature_data

    def calculate_precipitation_statistics(self, weather_data):
        """
        Calculates all precipitation statistics from database weather data
        :param weather_data:
        :param threshold_high:
        :param threshold_low:
        :return:
        """

        df_weather = pd.DataFrame(list(weather_data))

        total_precip = df_weather['precipitation'].sum()
        avg_precip = df_weather['precipitation'].mean()

        df_weather['day'] = df_weather['date'].dt.date
        total_by_day = df_weather.groupby('date')['precipitation'].sum().to_dict()
        total_by_day = {d.strftime('%Y-%m-%d'): v for d, v in total_by_day.items()}

        days_with_precipitation = (df_weather.groupby('day')['precipitation'].sum() > 0).sum()

        max_row = df_weather.loc[df_weather['precipitation'].idxmax()]
        max_precip = {
            "value": max_row['precipitation'],
            "date": max_row['date'].date().isoformat()
        }

        precipitation_data = {
            "precipitation": {
                "total": round(total_precip, 2),
                "total_by_day": {k: round(v, 2) for k, v in total_by_day.items()},
                "days_with_precipitation": int(days_with_precipitation),
                "max": max_precip,
                "average": round(avg_precip, 2)
            }
        }

        return precipitation_data

    def calculate_general_statistics(self, weather_data, threshold_low, threshold_high):
        df_weather = pd.DataFrame(list(weather_data))
        general_statistics = dict()
        for location_id, df_loc in df_weather.groupby('location_id'):
            try:
                locality_name = Location.objects.get(id=location_id).locality
            except Location.DoesNotExist:
                locality_name = f"ID_{location_id}"  # if location not exist
            general_statistics[locality_name] = self.calculate_statistics_by_location(df_weather,
                                                                            threshold_low,
                                                                            threshold_high)
        return general_statistics

    def calculate_statistics_by_location(self, df_weather, threshold_low: float, threshold_high: float):
        """
                Calculates all statistics by location from database weather data
                :param weather_data:
                :return:
                """

        avg_temp = df_weather['temperature'].mean()
        avg_by_day = df_weather.groupby('date')['temperature'].mean().to_dict()
        avg_by_day = {d.strftime('%Y-%m-%d'): v for d, v in avg_by_day.items()}

        max_row = df_weather.loc[df_weather['temperature'].idxmax()]
        min_row = df_weather.loc[df_weather['temperature'].idxmin()]

        hours_above = np.sum(df_weather['temperature'] > threshold_high)
        hours_below = np.sum(df_weather['temperature'] < threshold_low)

        total_precip = df_weather['precipitation'].sum()
        avg_precip = df_weather['precipitation'].mean()

        total_by_day = df_weather.groupby('date')['precipitation'].sum().to_dict()
        total_by_day = {d.strftime('%Y-%m-%d'): v for d, v in total_by_day.items()}

        days_with_precip = (df_weather.groupby('date')['precipitation'].sum() > 0).sum()
        max_p_row = df_weather.loc[df_weather['precipitation'].idxmax()]

        statistics_by_location_data = {
            "temperature": {
                "average": round(avg_temp, 1),
                "average_by_day": avg_by_day,
                "max": {
                    "value": round(max_row['temperature'], 1),
                    "date_time": max_row['date'].isoformat(timespec='minutes')
                },
                "min": {
                    "value": round(min_row['temperature'], 1),
                    "date_time": min_row['date'].isoformat(timespec='minutes')
                },
                "hours_above_threshold": int(hours_above),
                "hours_below_threshold": int(hours_below)
            },
            "precipitation": {
                "total": round(total_precip, 2),
                "total_by_day": {k: round(v, 2) for k, v in total_by_day.items()},
                "days_with_precipitation": int(days_with_precip),
                "max": {
                    "value": round(max_p_row['precipitation'], 2),
                    "date": max_p_row['date'].date().isoformat()
                },
                "average": round(avg_precip, 2)
            }
        }

        return statistics_by_location_data
