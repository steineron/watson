import datetime
from django.db import models


# Create your models here.
from django.utils import timezone


class User(models.Model):
    """
    A user model, a user can be authenticated, identified, contacted etc.
    A user can ask questions, can answer questions etc.
    """
    user_name = models.CharField(max_length=100)


class Location(models.Model):
    """
    people ask questions about locations
    """
    name = models.CharField(max_length=256)
    longitude = models.FloatField()
    latitude = models.FloatField()


class Question(models.Model):
    """
    A question that was asked. who asked, when and what answers did it get
    """
    QUESTION_TYPES = (
        ('YN', 'Yes/ No'),
        ('MC', 'Multiple Choice'),
        ('OP', 'Open-ended')
    )
    type = models.CharField(max_length=2, default='OP')
    by_user = models.ForeignKey(User)
    about_location = models.ForeignKey(Location)
    body = models.CharField(max_length=1024)
    posted_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    def was_posted_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.posted_date <= now

    was_posted_recently.admin_order_field = 'posted_date'
    was_posted_recently.boolean = True
    was_posted_recently.short_description = 'Posted recently?'


class Answer(models.Model):
    """
    an answer to a question.
    """
    to_question = models.ForeignKey(Question)
    body = models.CharField(max_length=1024)
    provided_by = models.ForeignKey(User)
    provided_on = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
