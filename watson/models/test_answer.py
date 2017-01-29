from unittest import TestCase

from watson.models import Answer
from watson.models import User
from watson.models import Question

from watson.models import Location
from watson.models.questions import YesNoQuestion


class TestAnswer(TestCase):
    def setUp(self):
        self.asking = User.objects.create(user_name='asking')
        self.answerer = User.objects.create(user_name='answering')
        self.location = Location.objects.create(name='somewhere', latitude=123.4, longitude=567.8)
        self.question = YesNoQuestion.objects.create(
                                                body='watson somewhere?',
                                                about_location=self.location,
                                                by_user=self.asking)

    def tearDown(self):
        self.asking.delete()
        self.answerer.delete()
        self.location.delete()
        self.question.delete()

    def test_that_answer(self):
        answer = Answer.objects.create(provided_by=self.answerer, body='Y', to_question=self.question)
        self.assertEqual(answer.body, 'Y')
