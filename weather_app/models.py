from django.db import models


"""
The models that make up the ORM and communicate the weather_app with database.
"""


class Location(models.Model):
    locality = models.CharField(max_length=100)
    lat = models.FloatField()
    long = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.locality

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['locality'],
                name='unique_locality'
            )
        ]


class HourlyWeatherData(models.Model):
    temperature = models.FloatField()
    precipitation = models.FloatField(null=True, blank=True)
    date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="hourly_data")

    def __str__(self):
        return f"{self.date} - {self.location.locality}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['location', 'date'],
                name='unique_location_date'
            )
        ]

