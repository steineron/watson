from django.db import models

from watson.models import Question
from watson.models import User


class Answer(models.Model):
    """
    an answer to a question.
    """
    answer = models.CharField(max_length=1024)
    provided_by = models.ForeignKey(User)
    provided_on = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    to_question = models.ForeignKey(Question)

    class Meta:
        app_label = "watson"

