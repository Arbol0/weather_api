import pytest
from datetime import datetime
from django.db import IntegrityError
from weather_app.models import Location, HourlyWeatherData
from weather_app.services.model_handler import ModelHandler


@pytest.mark.django_db
def test_insert_location_success():
    messages = []
    handler = ModelHandler(messages)

    loc = handler.insert_location("Madrid", 40.4168, -3.7038)

    assert loc is not None
    assert loc.locality == "Madrid"
    assert loc.lat == 40.4168
    assert loc.long == -3.7038
    assert messages == []


@pytest.mark.django_db
def test_insert_location_unique_constraint():
    messages = []
    handler = ModelHandler(messages)

    # Inserta la primera vez
    loc1 = handler.insert_location("Madrid", 40.4168, -3.7038)
    assert loc1 is not None

    # Intentar insertar otra vez con la misma localidad
    loc2 = handler.insert_location("Madrid", 41.0, -4.0)

    assert loc2 is None
    assert len(messages) == 1
    assert "unique_locality" in messages[0]


@pytest.mark.django_db
def test_insert_hourly_weather_data_success():
    messages = []
    handler = ModelHandler(messages)

    loc = handler.insert_location("Barcelona", 41.3851, 2.1734)

    data = handler.insert_hourly_weather_data(
        temperature=25.0,
        precipitation=0.0,
        date=datetime(2025, 10, 28, 15),
        location=loc
    )

    assert data is not None
    assert data.temperature == 25.0
    assert data.precipitation == 0.0
    assert data.location == loc
    assert messages == []


@pytest.mark.django_db
def test_insert_hourly_weather_data_unique_constraint():
    messages = []
    handler = ModelHandler(messages)

    loc = handler.insert_location("Valencia", 39.4699, -0.3763)

    # Inserta primera vez
    data1 = handler.insert_hourly_weather_data(20.0, 0.0, datetime(2025, 10, 28, 10), loc)
    assert data1 is not None

    # Intentar insertar la misma fecha y location
    data2 = handler.insert_hourly_weather_data(21.0, 0.5, datetime(2025, 10, 28, 10), loc)

    assert data2 is None
    assert len(messages) == 1
    assert "unique_location_date" in messages[0]


@pytest.mark.django_db
def test_get_all_locations():
    messages = []
    handler = ModelHandler(messages)

    handler.insert_location("Sevilla", 37.3886, -5.9823)
    handler.insert_location("Bilbao", 43.2630, -2.9349)

    locations = handler.get_all_locations()

    assert len(locations) == 2
    names = [loc['locality'] for loc in locations]
    assert "Sevilla" in names
    assert "Bilbao" in names


@pytest.mark.django_db
def test_get_all_weather_data():
    messages = []
    handler = ModelHandler(messages)

    loc = handler.insert_location("Granada", 37.1773, -3.5986)
    handler.insert_hourly_weather_data(15.0, 0.0, datetime(2025, 10, 28, 9), loc)
    handler.insert_hourly_weather_data(16.0, 0.2, datetime(2025, 10, 28, 10), loc)

    data = handler.get_all_weather_data()

    assert len(data) == 2
    temps = [d['temperature'] for d in data]
    assert 15.0 in temps
    assert 16.0 in temps
