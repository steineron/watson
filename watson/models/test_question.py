from unittest import TestCase

from watson.models import Location
from watson.models import User
from watson.models.questions import YesNoQuestion, Question


class TestQuestion(TestCase):
    def setUp(self):
        self.asking = User(user_name='asking')
        self.asking.save()

        self.answerer = User(user_name='answering')
        self.answerer.save()

        self.location = Location(name='somewhere', latitude=123.4, longitude=567.8)
        self.location.save()

        self.yn_question = Question(_type='YN', body='watson somewhere?')
        self.yn_question.about_location = self.location
        self.yn_question.by_user = self.asking
        self.yn_question.save()

    def tearDown(self):
        self.asking.delete()
        self.answerer.delete()
        self.location.delete()
        self.yn_question.delete()

    def test_that_question_created(self):
        question = YesNoQuestion.objects.get()
        self.assertEqual(question._type, 'YN')
        self.assertEqual(question.body, 'watson somewhere?')
