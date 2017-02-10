import datetime

from django.db import models
from django.utils import timezone

from watson.models import User
from watson.models.locations import Location


QUESTION_TYPES = (
        ('YN', 'Yes No'),
        ('MC', 'Multiple Choice'),
        ('OP', 'Open ended')
    )


class Question(models.Model):
    """
    A question that was asked. who asked, when and what answers did it get
    """

# I had to comment the assertion in
# /Users/steinerro/.virtualenvs/django_for_watson/lib/python3.5/site-packages/graphene/types/typemap.py
# lines 71-3
# to make the choices work

    _question_type = models.CharField(max_length=2, choices=QUESTION_TYPES, default='OP')
    uid = models.CharField(max_length=512, unique=True, primary_key=True)
    by_user = models.ForeignKey(User)
    about_location = models.ForeignKey(Location)
    body = models.CharField(max_length=1024)
    posted_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "watson"

    def __str__(self):
        return self.body

    def was_posted_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.posted_date <= now

    was_posted_recently.admin_order_field = 'posted_date'
    was_posted_recently.boolean = True
    was_posted_recently.short_description = 'Posted recently?'

#
# class YesNoQuestion(Question):
#     def __init__(self, *args, **kwargs):
#         super(YesNoQuestion, self).__init__(*args, **kwargs)
#         self._question_type = 'YN'
#
#
# class OpenEndedQuestion(Question):
#     def __init__(self, *args, **kwargs):
#         super(OpenEndedQuestion, self).__init__(*args, **kwargs)
#         self._question_type = 'OP'
