from django.db import models

from watson.models import User
from watson.models.questions import Question


class Answer(models.Model):
    """
    an answer to a question.
    """
    to_question = models.ForeignKey(Question)
    body = models.CharField(max_length=1024)
    provided_by = models.ForeignKey(User)
    provided_on = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    class Meta:
        app_label = "watson"

