from django.db import models


class Location(models.Model):
    """
    people ask questions about locations
    """
    name = models.CharField(max_length=256)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        app_label = "watson"
