
from weather_app.models import Location
from weather_app.models import HourlyWeatherData

class ModelHandler:
    """
    Handler that manages all queries and operations to the database models.
    """

    def __init__(self, messages: list):
        self.messages = messages

    def insert_location(self, locality: str, latitude: float, longitude: float):
        """
        Insert one record of location.
        :param locality:
        :param latitude:
        :param longitude:
        :return:
        """
        try:
            location = Location.objects.create(locality=locality, lat=latitude, long=longitude)
        except Exception as e:
            self.messages.append(f'error: {e}')
            location = None
        return location

    def insert_hourly_weather_data(self, temperature, precipitation, date, location):
        """
        Insert one record of hourly weather data.
        :param temperature:
        :param precipitation:
        :param date:
        :param location:
        :return:
        """
        try:
            hourly_weather_data = HourlyWeatherData.objects.create(temperature=temperature,
                                                                      precipitation=precipitation,
                                                                      date=date,
                                                                      location=location)
        except Exception as e:
            self.messages.append(f'error: {e}')
            hourly_weather_data = None
        return hourly_weather_data

    def insert_user_queries(self):
        pass

    def get_all_locations(self):
        """
        Obtains all location records
        :return:
        """
        all_location = Location.objects.all().values()
        return all_location

    def get_all_weather_data(self):
        """
        Obtains all weather data records
        :return:
        """
        all_weather_data = HourlyWeatherData.objects.all().values()
        return all_weather_data

    def get_user_queries(self):
        pass



