from django.db import models

# Create your models here.
class Location(models.Model):
    locality = models.CharField(max_length=100)
    lat = models.FloatField()
    long = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)  # opcional

    def __str__(self):
        return self.locality


class HourlyWeatherData(models.Model):
    temperature = models.FloatField()
    precipitation = models.FloatField(null=True, blank=True)  # si luego quieres añadir precipitación
    pressure = models.FloatField()  # surface_pressure
    date = models.DateTimeField()
    location: Location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="hourly_data")

    def __str__(self):
        return f"{self.date} - {self.location.locality}"

