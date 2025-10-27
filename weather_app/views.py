
from rest_framework.views import APIView
from rest_framework.response import Response

from weather_app.services.meteo_api_handler import MeteoApiHandler
from weather_app.services.model_handler import ModelHandler
from weather_app.serializers import LocationSerializer, HourlyWeatherDataSerializer


class WeatherController(APIView):

    def __init__(self):
        self.messages = list()
        self.model_handler = ModelHandler(self.messages)
        self.meteo_api_handler = MeteoApiHandler(self.messages)

    def post(self, request):

        status = 200
        parameters = request.data
        start_date = None
        end_date = None
        city_name = None
        try:
            start_date = parameters['start_date']
            if start_date is None:
                self.messages.append('error : start_date is null')
                status = 400
            end_date = parameters['end_date']
            if end_date is None:
                self.messages.append('error : end_date is null')
                status = 400
            city_name = parameters['city_name']
            if city_name is None:
                self.messages.append('error : city_name is null')
                status = 400

        except Exception as e:
            self.messages.append(f'error : Invalid parameters {e}')

        coordinates = self.meteo_api_handler.get_coordinates(city_name=city_name)
        if coordinates:
            temperatures, precipitations, times = self.meteo_api_handler.get_hourly_weather_data(
                                                      latitude=coordinates['lat'],
                                                      longitude=coordinates['lon'],
                                                      start_date=start_date,
                                                      end_date=end_date)

            location_model = self.model_handler.insert_location(
                                          locality=city_name,
                                          latitude=coordinates['lat'],
                                          longitude=coordinates['lon'])

            if location_model:
                hourly_weather_data_models = list()
                for i in range(len(times)):
                    hourly_weather_data_model = self.model_handler.insert_hourly_weather_data(
                        temperature=temperatures[i],
                        precipitation=precipitations[i],
                        date=times[i],
                        location=location_model
                    )
                    hourly_weather_data_models.append(hourly_weather_data_model)

            else:
                hourly_weather_data_models = None

            if location_model and hourly_weather_data_models:
                location_serialized = LocationSerializer(location_model)
                hourly_weather_data_serialized = HourlyWeatherDataSerializer(hourly_weather_data_models, many=True)
                result_data = {
                   'location':  location_serialized.data,
                   'hourly_weather_data': hourly_weather_data_serialized.data
                }
            else:
                self.messages.append('No inserted data in database')
                result_data = None
        else:
            self.messages.append('No coordinates for city name')
            result_data = None
        response = {
            'message': self.messages,
            'status': status,
            'result_data': result_data
        }
        return Response(response, status)

    def get(self, request, type):
        status = 200
        parameters = request.data
        start_date = None
        end_date = None
        city_name = None
        threshold_high = None
        threshold_low = None
        try:
            start_date = parameters['start_date']
            if start_date is None:
                self.messages.append('error : start_date is null')
                status = 400
            end_date = parameters['end_date']
            if end_date is None:
                self.messages.append('error : end_date is null')
                status = 400
            city_name = parameters['city_name']
            if city_name is None:
                self.messages.append('error : city_name is null')
                status = 400
            threshold_high = parameters['threshold_high']
            threshold_low = parameters['threshold_low']
        except Exception as e:
            self.messages.append(f'error : Invalid parameters {e}')

        if (type == "temperature"):
            all_weather_data = self.model_handler.get_all_weather_data()
            filtered_weather_data = all_weather_data.filter(location__locality=city_name,
                                                            date__range=(start_date, end_date))
            temperature_data = self.meteo_api_handler.calculate_temperature_statistics(
                weather_data=filtered_weather_data,
                threshold_high=threshold_high,
                threshold_low=threshold_low
            )
            response = {
                'message': self.messages,
                'status': status,
                'result_data': temperature_data
            }
            return Response(response, status)

        elif (type == "precipitation"):
            all_weather_data = self.model_handler.get_all_weather_data()
            filtered_weather_data = all_weather_data.filter(location__locality=city_name,
                                                            date__range=(start_date, end_date))
            precipitation_data = self.meteo_api_handler.calculate_precipitation_statistics(filtered_weather_data)
            response = {
                'message': self.messages,
                'status': status,
                'result_data': precipitation_data
            }
            return Response(response, status)

        elif (type == "general_statistics"):
            all_weather_data = self.model_handler.get_all_weather_data()
            general_statistics = self.meteo_api_handler.calculate_general_statistics(
                weather_data=all_weather_data,
                threshold_high=threshold_high,
                threshold_low=threshold_low
            )

            response = {
                'message': self.messages,
                'status': status,
                'result_data': general_statistics
            }
            return Response(response, status)

        else:
            self.messages.append('The url doesnt exits')

