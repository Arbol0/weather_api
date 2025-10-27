WeatherApi
-

WeatherApi es la api con la que se hacen consultas a los endpoints de open-weather:
```https://geocoding-api.open-meteo.com/v1/search```
```https://archive-api.open-meteo.com/v1/archive``` 

Y con 4 endpoints se cargan los datos en una base de datos local de 'sqlite', además de calcular estadisticas 
de temperatura, preciptación o ambas según una localización y un rango de fechas.


Pasos para la instalación:
-
- Clonar repositorio en local.
- Renombrar .env.example a .env y añadir los valores.
- Ejecutar pipenv para instalar librerias en la raiz del proyecto:
```pipenv shell```
```pipenv install```

Pasos para la ejecucion:
-
- Ejecutar en la raiz del proyecto: 
```python manage.py runserver 0.0.0.0:8000```
- Una vez iniciada la api, se pueden ejecutar los 4 enpoints como en estos ejemplos desde la terminal:
- ```curl -X POST -H "Content-Type: application/json" -d '{"start_date": "2025-10-01", "end_date": "2025-10-01", "city_name": "madrid"}' http://localhost:8000/weather_app/weather_data/```
- ```curl -X GET -H "Content-Type: application/json" -d '{"start_date": "2025-10-01", "end_date": "2025-10-01", "city_name": "madrid", "threshold_high": 30, "threshold_low": 0}' http://localhost:8000/weather_app/temperature/```
- ```curl -X GET -H "Content-Type: application/json" -d '{"start_date": "2025-10-01", "end_date": "2025-10-01", "city_name": "madrid"}' http://localhost:8000/weather_app/precipitation/```
- ```curl -X GET -H "Content-Type: application/json" -d '{"start_date": "2025-10-01", "end_date": "2025-10-01", "city_name": "madrid", "threshold_high": 30, "threshold_low": 0}' http://localhost:8000/weather_app/general_statistics/```

Pendiente:
-
- Handler para la seguridad de los endpoints utilizando la libreria de ```rest_framework.permissions``` y ```rest_framework.authtoken.views```
- Tests unitatios para comprobar los calculos de las funciones de ApiHandler, los posibles duplicados de las operaciones de insercion y posibles errores en los parametros de entrada de los endpoints.
- Exponer la api desde un contenedor docker
