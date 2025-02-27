from django.db import models

# Create your models here.
class Location(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=255, db_column="city")
    country = models.CharField(max_length=100, db_column="country")
    iso3 = models.CharField(max_length=3, db_column="iso3")
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "location_data"
        managed = False