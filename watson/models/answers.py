from django.db import models

from watson.models import User
from watson.models.questions import YesNoQuestion, OpenEndedQuestion


class Answer(models.Model):
    """
    an answer to a question.
    """
    provided_by = models.ForeignKey(User)
    provided_on = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    class Meta:
        app_label = "watson"
        abstract = True

    def answer(self):
        pass

    answer.string = True


class YesNoAnswer(Answer):
    YES_NO_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No')
    )

    to_question = models.ForeignKey(YesNoQuestion)
    _answer = models.CharField(max_length=1, choices=YES_NO_CHOICES)

    def answer(self):
        return self._answer


class OpenEndedAnswer(Answer):
    to_question = models.ForeignKey(OpenEndedQuestion)
    _answer = models.CharField(max_length=1024)

    def answer(self):
        return self._answer
