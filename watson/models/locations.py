from django.db import models


class Location(models.Model):
    """
    people ask questions about locations
    """
    name = models.CharField(max_length=256)
    # id of google places api
    gp_id = models.CharField(max_length=512, unique=True, primary_key=True)
    description = models.CharField(max_length=2048, null=True)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        app_label = "watson"
