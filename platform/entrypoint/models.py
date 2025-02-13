from django.db import models

# Create your models here.

class LocationData(models.model):
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    iso3 = models.CharField(max_length=3)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.location}'