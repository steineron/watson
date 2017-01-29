import datetime

from django.db import models
from django.utils import timezone

from watson.models import User
from watson.models.locations import Location


class Question(models.Model):
    """
    A question that was asked. who asked, when and what answers did it get
    """
    QUESTION_TYPES = (
        ('YN', 'Yes/ No'),
        ('MC', 'Multiple Choice'),
        ('OP', 'Open-ended')
    )
    _type = models.CharField(max_length=2, choices=QUESTION_TYPES, default='OP')
    by_user = models.ForeignKey(User)
    about_location = models.ForeignKey(Location)
    body = models.CharField(max_length=1024)
    posted_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "watson"
        abstract = True

    def __str__(self):
        return self.body

    def was_posted_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.posted_date <= now

    was_posted_recently.admin_order_field = 'posted_date'
    was_posted_recently.boolean = True
    was_posted_recently.short_description = 'Posted recently?'


class YesNoQuestion(Question):
    def __init__(self, *args, **kwargs):
        super(YesNoQuestion, self).__init__(*args, **kwargs)
        self._type = 'YN'


class OpenEndedQuestion(Question):
    def __init__(self, *args, **kwargs):
        super(OpenEndedQuestion, self).__init__(*args, **kwargs)
        self._type = 'OP'
