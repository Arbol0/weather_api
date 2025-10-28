import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from datetime import datetime

from weather_app.services.meteo_api_handler import MeteoApiHandler


@pytest.fixture
def handler():
    return MeteoApiHandler(messages=[])


# --- TEST get_coordinates ---
@patch("weather_app.services.meteo_api_handler.requests.get")
def test_get_coordinates_success(mock_get, handler):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{"latitude": 40.4168, "longitude": -3.7038}]
    }
    mock_get.return_value = mock_response

    coords = handler.get_coordinates("Madrid")

    assert coords == {"lat": 40.4168, "lon": -3.7038}
    assert handler.messages == []

def test_get_coordinates_debug():
    messages = []
    handler = MeteoApiHandler(messages)

    # Mock requests.get
    with patch("weather_app.services.meteo_api_handler.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "results": [
                {"latitude": 40.4168, "longitude": -3.7038}  # Madrid
            ]
        }

        coords = handler.get_coordinates("Madrid")
        assert coords == {"lat": 40.4168, "lon": -3.7038}

@patch("weather_app.services.meteo_api_handler.requests.get")
def test_get_coordinates_not_found(mock_get, handler):
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    coords = handler.get_coordinates("CiudadInventada")

    assert coords is None
    assert "No se encontraron coordenadas" in handler.messages[0]


# --- TEST get_hourly_weather_data ---
@patch("weather_app.services.meteo_api_handler.requests.get")
def test_get_hourly_weather_data(mock_get, handler):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "hourly": {
            "temperature_2m": [10.0, 12.5, 11.0],
            "precipitation": [0.0, 1.2, 0.0],
            "time": ["2025-10-01T00:00", "2025-10-01T01:00", "2025-10-01T02:00"]
        }
    }
    mock_get.return_value = mock_response

    temps, precs, times = handler.get_hourly_weather_data(40.0, -3.0, "2025-10-01", "2025-10-02")

    assert temps == [10.0, 12.5, 11.0]
    assert precs == [0.0, 1.2, 0.0]
    assert len(times) == 3


# --- TEST calculate_temperature_statistics ---
def test_calculate_temperature_statistics(handler):
    data = [
        {"temperature": 10.0, "date": pd.Timestamp("2025-10-01 00:00")},
        {"temperature": 15.0, "date": pd.Timestamp("2025-10-01 01:00")},
        {"temperature": 8.0, "date": pd.Timestamp("2025-10-02 00:00")},
    ]
    stats = handler.calculate_temperature_statistics(data, threshold_high=14, threshold_low=9)

    temp = stats["temperature"]
    assert temp["average"] == pytest.approx(11.0, rel=1e-2)
    assert temp["max"]["value"] == 15.0
    assert temp["min"]["value"] == 8.0
    assert temp["hours_above_threshold"] == 1
    assert temp["hours_below_threshold"] == 1


# --- TEST calculate_precipitation_statistics ---
def test_calculate_precipitation_statistics(handler):
    data = [
        {"precipitation": 0.0, "date": pd.Timestamp("2025-10-01 00:00")},
        {"precipitation": 2.5, "date": pd.Timestamp("2025-10-01 01:00")},
        {"precipitation": 1.0, "date": pd.Timestamp("2025-10-02 00:00")},
    ]

    stats = handler.calculate_precipitation_statistics(data)
    precip = stats["precipitation"]

    assert precip["total"] == 3.5
    assert precip["days_with_precipitation"] == 2
    assert precip["max"]["value"] == 2.5
    assert precip["average"] == pytest.approx(1.17, rel=1e-2)


# --- TEST calculate_statistics_by_location ---
def test_calculate_statistics_by_location(handler):
    df = pd.DataFrame([
        {"temperature": 10.0, "precipitation": 0.0, "date": pd.Timestamp("2025-10-01 00:00")},
        {"temperature": 20.0, "precipitation": 2.5, "date": pd.Timestamp("2025-10-01 01:00")},
        {"temperature": 15.0, "precipitation": 1.0, "date": pd.Timestamp("2025-10-02 00:00")},
    ])

    stats = handler.calculate_statistics_by_location(df, threshold_low=9, threshold_high=18)

    assert stats["temperature"]["max"]["value"] == 20.0
    assert stats["precipitation"]["total"] == 3.5
    assert stats["precipitation"]["days_with_precipitation"] == 2


# --- TEST calculate_general_statistics ---
@patch("weather_app.services.meteo_api_handler.Location")
def test_calculate_general_statistics(mock_location, handler):
    mock_location.objects.get.side_effect = lambda id: type("Loc", (), {"locality": f"City{id}"})()

    data = [
        {"location_id": 1, "temperature": 10.0, "precipitation": 0.5, "date": pd.Timestamp("2025-10-01")},
        {"location_id": 1, "temperature": 12.0, "precipitation": 0.0, "date": pd.Timestamp("2025-10-02")},
        {"location_id": 2, "temperature": 14.0, "precipitation": 1.0, "date": pd.Timestamp("2025-10-01")},
    ]

    stats = handler.calculate_general_statistics(data, threshold_low=9, threshold_high=18)
    assert "City1" in stats
    assert "City2" in stats
    assert "temperature" in stats["City1"]
