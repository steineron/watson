from django.db import models


class User(models.Model):
    """
    A user model, a user can be authenticated, identified, contacted etc.
    A user can ask questions, can answer questions etc.
    """

    user_name = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=100)

    class Meta:
        app_label = "watson"
